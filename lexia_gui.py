import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import webbrowser
import requests

LEXIA_NAME = "lexia"
running = False
last_city = None

def log(text):
    output_area.config(state='normal')
    output_area.insert(tk.END, text + "\n")
    output_area.see(tk.END)
    output_area.config(state='disabled')

def talk(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
        log(f"{LEXIA_NAME.capitalize()}: {text}")
    except Exception as e:
        log(f"Error in talk(): {e}")

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source)
            command = listener.recognize_google(audio).lower()
            log(f"You said: {command}")
            return command
        except Exception:
            return ""

def get_weather(city):
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        return response.text
    except:
        return "Unable to fetch weather."

def run_lexia():
    global running, last_city
    while running:
        command = take_command()
        if not command:
            continue

        if 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {current_time}")

        elif 'google' in command:
            talk("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'youtube' in command:
            talk("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif any(greet in command for greet in ['hello','hi','hey','good morning','good afternoon','good evening']):
            talk(f"Hello! I am {LEXIA_NAME}. How can I help you?")

        elif 'weather' in command:
            if last_city:
                weather_info = get_weather(last_city)
                talk(weather_info)
            else:
                talk("Which city?")
                city = take_command()
                if city:
                    last_city = city
                    weather_info = get_weather(city)
                    talk(weather_info)
                else:
                    talk("I didn't catch the city name.")

        elif 'thank you' in command or 'thanks' in command:
            talk("You're welcome! Goodbye!")
            stop_listening()

        elif 'stop' in command or 'exit' in command or 'quit' in command:
            talk("Goodbye!")
            stop_listening()

        else:
            talk("Sorry, I didn't understand that.")

def start_listening():
    global running
    if not running:
        running = True
        threading.Thread(target=run_lexia).start()
        log(f"{LEXIA_NAME.capitalize()} started listening...")

def stop_listening():
    global running
    running = False
    log(f"{LEXIA_NAME.capitalize()} stopped.")

root = tk.Tk()
root.title("Lexia- Your AI,Your VOICE")
root.geometry("500x450")

start_btn = tk.Button(root, text="Start Listening", command=start_listening)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", command=stop_listening)
stop_btn.pack(pady=5)

output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled')
output_area.pack(pady=10)

command_entry = tk.Entry(root, width=50)
command_entry.pack(pady=5)

root.mainloop()
