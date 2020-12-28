import speech_recognition as sr
import tkinter as tk
from threading import Timer


class SpeechRecognition:
    def __init__(self):
        # print(sr.__version__)

        # create an instance of the Recognizer class that will recognize audio components
        self._r = sr.Recognizer()

        # # initialize a variable to get the audio file
        # file = sr.AudioFile("sample.wav")
        #
        # # continuously store the data of the audio file into a variable
        # with file as source:
        #     audio = r.record(source, duration=4)  # duration will tell only capture the audio up until "n" seconds
        #     next_audio = r.record(source, duration=4)  # this will capture the NEXT 4 seconds of the audio file
        #     offset_audio = r.record(source, offset=4)  # offsetting will skip the first "n" seconds
        #
        # # finally seek for any speech in the audio file (uses Google Speech API)
        # print(r.recognize_google(audio))
        #
        # # compare with audio with heavy noise in the background
        # file_two = sr.AudioFile("sample with noise.wav")
        #
        # with file_two as source:
        #     r.adjust_for_ambient_noise(source, duration=0.5)  # will adjust audio, but not completely perfect
        #     noisy_audio = r.record(source)
        #
        # print(r.recognize_google(noisy_audio, show_all=False))  # "show_all" will show all text-to-speech transcripts

        # speech recognition from mic audio
        # displays all the available microphone devices
        # print(sr.Microphone.list_microphone_names())

        # initialize a mic object
        self._mic = sr.Microphone()  # device_index can be used to configure which mic should be used

        for i in range(0, 1):
            print("Say something...")
            with self._mic as source:
                # r.adjust_for_ambient_noise(source)
                self._audio = self._r.listen(source)

            try:
                self._speech = f'You said: "{self._r.recognize_google(self._audio)}"\n'
                print(self._speech)
            except LookupError:
                print("Could not understand audio")

    def get_mic_audio(self):
        print("Say something...")
        with self._mic as source:
            self._audio = self._r.listen(source)

        try:
            self._speech = f'You said: "{self._r.recognize_google(self._audio)}"\n'
            print(self._speech)
        except LookupError:
            print("Could not understand audio")

        return self._speech

    def return_mic_audio(self):
        return self._speech


class SpeechRecognitionGUI:
    def __init__(self, root):
        self._backend = SpeechRecognition()

        root.title("Speech Recognition")
        root.configure(background="black")
        root.geometry("680x305")

        say_button = tk.Button(height=3, width=10, command=self.now_listening, text="Press To Talk")
        say_button.place(x=0, y=0)

        self._speech_text = self._backend.return_mic_audio()
        self._text_window = tk.Text(height=7, width=45, font=("Segoe Print", 15), fg="white", bg="black")
        self._text_window.insert(tk.END, self._speech_text)
        self._text_window.place(x=0, y=55)

        self._listening_label = tk.Label(height=1, text="", font=("Segoe Print", 15), fg="White",
                                         bg="Black", borderwidth=2, relief="solid")
        self._listening_label.place(x=90, y=10)

        root.mainloop()

    def now_listening(self):
        self._listening_label.configure(text="Listening...")
        self._text_window.delete('1.0', tk.END)

        t = Timer(0.5, self.get_audio_and_configure_text)
        t.start()

    def get_audio_and_configure_text(self):
        updated_speech = self._backend.get_mic_audio()
        updated_speech = updated_speech.replace("You said: ", '')

        self._text_window.insert(tk.END, updated_speech)

        self._listening_label.configure(text="")


if __name__ == "__main__":
    root = tk.Tk()
    s = SpeechRecognitionGUI(root)
