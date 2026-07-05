"""
AI Virtual Voice Assistant
--------------------------
A voice-command assistant that listens for speech, classifies intent,
and responds to task/system commands. Falls back to a text-input mode
if no microphone is available, so the logic can be tested without audio hardware.

Run with: python assistant.py
Add --text to run in text-only mode (no microphone needed):
    python assistant.py --text
"""

import sys
import datetime
import webbrowser

try:
    import speech_recognition as sr
    import pyttsx3
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


class VoiceAssistant:
    def __init__(self, text_mode: bool = False):
        self.text_mode = text_mode or not AUDIO_AVAILABLE
        self.commands = {}  # registry: keyword -> handler function
        self._register_default_commands()

        if not self.text_mode:
            self.engine = pyttsx3.engine = pyttsx3.init()
            self.recognizer = sr.Recognizer()

    def _register_default_commands(self):
        """Register built-in commands. Add more with self.register()."""
        self.tasks = []
        self.register(["time", "what time"], self.tell_time)
        self.register(["date", "today's date"], self.tell_date)
        self.register(["open google"], lambda q: self._open_site("https://google.com"))
        self.register(["open youtube"], lambda q: self._open_site("https://youtube.com"))
        self.register(["add task", "remind me to"], self.add_task)
        self.register(["my tasks", "show tasks", "what are my tasks"], self.list_tasks)
        self.register(["hello", "hi"], lambda q: "Hello! How can I help you?")
        self.register(["exit", "quit", "stop", "bye"], lambda q: "__EXIT__")

    def add_task(self, query: str) -> str:
        for trigger in ["add task", "remind me to"]:
            if trigger in query.lower():
                task = query.lower().split(trigger, 1)[1].strip()
                if task:
                    self.tasks.append(task)
                    return f"Added task: '{task}'. You now have {len(self.tasks)} task(s)."
        return "Please tell me what task to add, e.g. 'remind me to submit assignment'."

    def list_tasks(self, query: str) -> str:
        if not self.tasks:
            return "You have no tasks saved yet."
        listing = "; ".join(f"{i+1}. {t}" for i, t in enumerate(self.tasks))
        return f"Your tasks: {listing}"

    def register(self, keywords, handler):
        """Register a new command. keywords: list of trigger phrases."""
        for kw in keywords:
            self.commands[kw] = handler

    def classify_intent(self, query: str):
        """Very simple keyword-based intent matching.
        Returns the matching handler, or None if no command matches."""
        query_lower = query.lower()
        for keyword, handler in self.commands.items():
            if keyword in query_lower:
                return handler
        return None

    def tell_time(self, query: str) -> str:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    def tell_date(self, query: str) -> str:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}."

    def _open_site(self, url: str) -> str:
        webbrowser.open(url)
        return f"Opening {url}"

    def respond(self, query: str) -> str:
        """Process a query and return a text response."""
        handler = self.classify_intent(query)
        if handler:
            return handler(query)
        return "Sorry, I didn't understand that command."

    def speak(self, text: str):
        print(f"Assistant: {text}")
        if not self.text_mode:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self) -> str:
        """Capture speech from the microphone and return recognized text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "__ERROR__"

    def run(self):
        mode = "text" if self.text_mode else "voice"
        print(f"Voice Assistant started in {mode} mode. Say/type 'exit' to quit.\n")
        while True:
            if self.text_mode:
                query = input("You: ")
            else:
                query = self.listen()
                if query == "__ERROR__":
                    self.speak("Speech service is unavailable right now.")
                    continue
                if not query:
                    continue

            response = self.respond(query)
            if response == "__EXIT__":
                self.speak("Goodbye!")
                break
            self.speak(response)


if __name__ == "__main__":
    text_mode = "--text" in sys.argv
    assistant = VoiceAssistant(text_mode=text_mode)
    assistant.run()
