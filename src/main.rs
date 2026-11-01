use jack::{Client, ClientOptions, Control, MidiOut, ProcessHandler, ProcessScope, RawMidi};
use std::sync::mpsc::{channel, Receiver};
use std::time::Duration;

const NOTE_ON: u8 = 0x90;
const NOTE_OFF: u8 = 0x80;
const VELOCITY: u8 = 0x64;

// 1. Define a clean, thread-safe structure to handle JACK events
struct MidiGenerator {
    midi_port: jack::Port<MidiOut>,
    receiver: Receiver<[u8; 3]>,
}

impl ProcessHandler for MidiGenerator {
    fn process(&mut self, _: &Client, process_scope: &ProcessScope) -> Control {
        // Create an explicit writer for our MIDI output port
        let mut writer = self.midi_port.writer(process_scope);

        // Drain any pending messages from our thread-safe cross-beam channel
        while let Ok(midi_bytes) = self.receiver.try_recv() {
            let event = RawMidi {
                time: 0, // Trigger immediately at the start of this buffer cycle
                bytes: &midi_bytes,
            };
            let _ = writer.write(&event);
        }

        Control::Continue
    }
}

fn main() {
    // 2. Initialize a JACK Client. PipeWire automatically captures this and presents it as a native node!
    let (client, _status) = Client::new("Rust-MIDI-Generator", ClientOptions::NO_START_SERVER)
        .expect("Failed to initialize JACK/PipeWire client");

    // 3. Register a clean, type-safe MIDI Output Port
    let midi_port = client
        .register_port("midi_out", MidiOut::default())
        .expect("Failed to register MIDI out port");

    // 4. Create an MPSC channel to safely communicate note generation from our main thread
    let (sender, receiver) = channel::<[u8; 3]>();

    let handler = MidiGenerator { midi_port, receiver };

    // 5. Activate the processing loop graph context
    let _active_client = client
        .activate_async((), handler)
        .expect("Failed to activate audio graph listener");

    println!("High-level MIDI Generator started via PipeWire-JACK layer.");

    // 6. Drive the timing timeline sequence purely using safe standard Rust loops
    let mut current_note = 60;
    loop {
        // Send Note On
        let _ = sender.send([NOTE_ON, current_note, VELOCITY]);
        std::thread::sleep(Duration::from_millis(500));

        // Send Note Off
        let _ = sender.send([NOTE_OFF, current_note, 0]);
        std::thread::sleep(Duration::from_millis(500));

        // Cycle through standard octaves smoothly
        current_note += 1;
        if current_note > 72 {
            current_note = 60;
        }
    }
}

