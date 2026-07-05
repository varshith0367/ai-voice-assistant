# AI Virtual Voice Assistant

A Python voice-command assistant that listens for speech, classifies intent using a keyword-based command registry, and responds to task and system commands (time, date, opening websites, greetings).

Includes a **text-only mode** so the core logic can be run and tested without a microphone or speakers.

## Features

- **Speech recognition** via Google's speech API (through the `SpeechRecognition` library)
- **Text-to-speech** responses via `pyttsx3`
- **Command registry pattern** — commands are registered as keyword → handler pairs, making it easy to add new commands without touching the core loop
- **Text mode fallback** — run entirely by typing, no audio hardware required

## Tech stack

- Python
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/) (offline text-to-speech)

## Running locally

**Voice mode** (requires a working microphone and speakers, plus `pyaudio`):
```bash
pip install -r requirements.txt
python assistant.py
```

**Text mode** (no microphone needed — good for testing or if audio isn't set up):
```bash
python assistant.py --text
```

## Example commands

- "what time is it"
- "what's today's date"
- "open google"
- "open youtube"
- "hello"
- "exit" (to quit)

## Adding new commands

Commands are registered in `_register_default_commands()` using:
```python
self.register(["keyword one", "keyword two"], handler_function)
```
Add a new method for your handler and register it the same way — no need to modify the main loop.

## Notes

This is a personal/academic project. Speech recognition accuracy depends on the `SpeechRecognition` library's Google Web Speech API, which requires an internet connection for voice mode.
