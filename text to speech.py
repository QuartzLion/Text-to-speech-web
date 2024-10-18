import threading
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Progressbar
from gtts import gTTS
import pygame  # For pause and resume control
import os

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Global variables to manage play, pause, and resume state
paused = False
current_audio_file = None

# Function to handle text-to-speech and play audio
def text_to_speech():
    global current_audio_file, paused

    input_text = text_entry.get()  # Get the text from the text field
    language = language_selector.get()  # Get selected language
    slow = speed_selector.get() == "Slow"  # Check speed selection

    if input_text.strip() == "":
        status_label.config(text="Please enter some text.", fg="red")
        return

    # Disable buttons and show processing status
    status_label.config(text="Processing...", fg="blue")
    progress_bar.start()
    speak_button.config(state=DISABLED)
    pause_button.config(state=DISABLED)
    resume_button.config(state=DISABLED)

    def process_speech():
        global current_audio_file, paused

        try:
            # Generate speech from the input text
            tts = gTTS(text=input_text, lang=language, slow=slow)
            current_audio_file = "output.mp3"
            tts.save(current_audio_file)

            # Play the generated audio file
            status_label.config(text="Playing the audio...", fg="green")
            pygame.mixer.music.load(current_audio_file)
            pygame.mixer.music.play()

            # Enable Pause and Resume buttons during playback
            pause_button.config(state=NORMAL)
            resume_button.config(state=DISABLED)

            while pygame.mixer.music.get_busy():  # Wait until audio is playing
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            # Reset state after playback
            status_label.config(text="Ready", fg="green")
            speak_button.config(state=NORMAL)
            progress_bar.stop()

        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
            speak_button.config(state=NORMAL)
            progress_bar.stop()

    # Run the speech generation and playback in a separate thread
    threading.Thread(target=process_speech).start()

# Function to load text from a file
def load_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            text_entry.delete(0, END)
            text_entry.insert(END, file_content)

# Pause the audio playback
def pause_audio():
    global paused
    paused = True
    status_label.config(text="Audio Paused", fg="orange")
    pause_button.config(state=DISABLED)
    resume_button.config(state=NORMAL)

# Resume the audio playback
def resume_audio():
    global paused
    paused = False
    status_label.config(text="Resuming Audio", fg="green")
    pause_button.config(state=NORMAL)
    resume_button.config(state=DISABLED)

# Exit the application
def exit_application():
    pygame.mixer.music.stop()  # Stop any playing audio
    root.destroy()  # Close the application window

# Creating the main window
root = Tk()
root.title("Enhanced Text-to-Speech App with Pause, Resume, and Exit")
root.geometry("500x450")
root.resizable(True, True)
root.configure(bg='#f0f0f0')

# Title Label
title_label = Label(root, text="Text-to-Speech Converter", font=("Helvetica", 16, "bold"), bg='#f0f0f0', fg='#333')
title_label.pack(pady=20)

# Frame for Input Text
input_frame = Frame(root, bg='#f0f0f0')
input_frame.pack(pady=10)

# Text Entry
text_entry = Entry(input_frame, width=40, font=("Helvetica", 12), bd=3)
text_entry.grid(row=0, column=0, padx=10)

# Load Text File Button
load_file_button = Button(input_frame, text="Load from File", font=("Helvetica", 10), bg="#FF8C00", fg="white", command=load_text_file)
load_file_button.grid(row=0, column=1, padx=10)

# Language Selection Dropdown
language_selector = Combobox(root, values=["en", "es", "fr", "de", "hi"], font=("Helvetica", 10), width=10)
language_selector.current(0)  # Default to English
language_selector.pack(pady=10)

# Speed Selection Dropdown
speed_selector = Combobox(root, values=["Normal", "Slow"], font=("Helvetica", 10), width=10)
speed_selector.current(0)  # Default to Normal speed
speed_selector.pack(pady=10)

# Speak Button
speak_button = Button(root, text="Convert to Speech", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=text_to_speech)
speak_button.pack(pady=10)

# Pause Button
pause_button = Button(root, text="Pause", font=("Helvetica", 12, "bold"), bg="#FF6347", fg="white", state=DISABLED, command=pause_audio)
pause_button.pack(pady=5)

# Resume Button
resume_button = Button(root, text="Resume", font=("Helvetica", 12, "bold"), bg="#4682B4", fg="white", state=DISABLED, command=resume_audio)
resume_button.pack(pady=5)

# Progress Bar for Visual Feedback
progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='indeterminate')
progress_bar.pack(pady=10)

# Status Label
status_label = Label(root, text="Enter your text and click the button.", font=("Helvetica", 10), bg='#f0f0f0', fg="blue")
status_label.pack(pady=5)

# Exit Button
exit_button = Button(root, text="Exit", font=("Helvetica", 12, "bold"), bg="#D32F2F", fg="white", command=exit_application)
exit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
