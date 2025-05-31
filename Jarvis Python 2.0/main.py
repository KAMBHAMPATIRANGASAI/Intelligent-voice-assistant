import datetime #For handling date and time operations.
import os #To perform operating system interactions and to manipulate system-specific parameters and functions.
import sys #
import time #To manage time-related functions.
import webbrowser #To open web pages in the default browser.
import pyautogui #For simulating user interface actions like mouse movements and keyboard presses.
import pyttsx3  #To convert text to speech, allowing the assistant to respond vocally.
import speech_recognition as sr #To recognize spoken words and convert them into text.
import json #For data serialization, enabling storage and retrieval of structured information.
import pickle
import random #For selecting random items, like jokes.
import numpy as np #For numerical computations, particularly when working with arrays.
import psutil #To monitor system usage such as CPU and battery statistics.
import requests #For making HTTP requests to external APIs for news and weather information.
from tensorflow.keras.models import load_model #For loading and utilizing machine learning models to understand user queries.
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tkinter as tk #For creating a graphical user interface (GUI)
from tkinter import scrolledtext
import threading
import tkinter.font as tkFont

# Load intents and models
with open(r"C:\journal\NLP\Multiverse_of_100-_data_science_project_series-main\Multiverse_of_100-_data_science_project_series-main\Jarvis Python 2.0\intents.json") as file:
    data = json.load(file)

model = load_model(r"C:\journal\NLP\Multiverse_of_100-_data_science_project_series-main\Multiverse_of_100-_data_science_project_series-main\Jarvis Python 2.0\chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open(r"C:\journal\NLP\Multiverse_of_100-_data_science_project_series-main\Multiverse_of_100-_data_science_project_series-main\Jarvis Python 2.0\label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Initialize tkinter root window
root = tk.Tk()
root.title("Voice Assistant")
#root.attributes("-fullscreen", True)  # Set window to fullscreen

# Define a larger font size
font_size = 25  # Adjust as necessary
font = tkFont.Font(size=font_size)

# Create a scrolled text widget for displaying commands and responses with increased font size
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=font)
text_area.grid(column=0, row=0, padx=10, pady=10)

# Create a label for displaying time with enlarged font
time_label = tk.Label(root, text="", font=("Helvetica", font_size))
time_label.grid(column=0, row=1, padx=10, pady=10)

# Function to toggle fullscreen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Bind <F11> key to toggle fullscreen on and off
#root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", toggle_fullscreen)  # Allow Escape to exit fullscreen

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

def speak(text):
    # Update the text area with the assistant's response
    text_area.insert(tk.END, f"{text}\n")  # Display only the response
    text_area.see(tk.END)  # Scroll to the end

    # Start a new thread to handle speech
    threading.Thread(target=thread_speak, args=(text,)).start()

def thread_speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)  # This will record the audio
    
    try:
        query = r.recognize_google(audio, language='en-in')  # Recognize the speech
        text_area.insert(tk.END, f"You: {query}\n")  # Display the user's query
        text_area.see(tk.END)  # Scroll to the end
        print("\rUser said: ", query)
    except Exception:
        print("Say that again please")
        return "None"
    return query.lower()


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    return day_dict.get(day, "Unknown Day")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()
    if 0 <= hour < 12:
        response = f"Good morning Boss, it's {day} and the time is {t}"
    elif 12 <= hour < 16:
        response = f"Good afternoon Boss, it's {day} and the time is {t}"
    else:
        response = f"Good evening Boss, it's {day} and the time is {t}"
    
    speak(response)
    
    # Update the time label with the current time
    time_label.config(text=f"Developed By Ranga Sai")

def social_media(command):
    if 'facebook' in command:
        speak("Opening your Facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("Opening your WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'linkedin' in command:
        speak("Opening your LinkedIn")
        webbrowser.open("https://www.linkedin.com/")
    elif 'instagram' in command:
        speak("Opening your Instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found.")

def schedule():
    day = cal_day().lower()
    speak("Boss, today's schedule is ")
    week = {
        "monday": "Boss, from 9:30 to 10:20 AM, you have Machine Learning. From 10:20 to 11:10 AM, you have Advanced SQL. From 11:10 AM to 12:50 PM, you have a break. From 12:50 to 2:10 PM, you have CRT. From 2:10 to 3:50 PM, you have Web Mining.",
        "tuesday": "Boss, from 9:30 to 10:20 AM, you have Advanced SQL. From 10:20 to 11:10 AM, you have Advanced SQL (SL). From 11:10 AM to 12:00 PM, you have a free slot. From 12:00 to 12:50 PM, you have Machine Learning. From 12:50 to 2:10 PM, you have a break. From 2:10 to 3:50 PM, you have Web Mining and CRT.",
        "wednesday": "Boss, from 9:30 to 10:20 AM, you have French & German. From 10:20 AM to 12:00 PM, you have a free slot. From 12:00 to 12:50 PM, you have a break. From 12:50 to 2:10 PM, you have Machine Learning Lab. From 2:10 to 3:50 PM, you have CRT.",
        "thursday": "Boss, from 9:30 to 10:20 AM, you have Web Mining (SL). From 10:20 to 11:10 AM, you have Web Mining Lab. From 11:10 AM to 12:00 PM, you have a free slot. From 12:00 to 12:50 PM, you have Natural Language Processing. From 12:50 to 2:10 PM, you have a break. From 2:10 to 3:50 PM, you have Natural Language Processing Lab and CRT.",
        "friday": "Boss, from 9:30 to 10:20 AM, you have French & German. From 10:20 to 11:10 AM, you have Advanced SQL Lab. From 11:10 AM to 12:50 PM, you have a break. From 12:50 to 2:10 PM, you have Machine Learning (SL). From 2:10 to 3:50 PM, you have Web Mining Lab and CRT.",
        "saturday": "Boss, today you have extra time for personal learning and project work. Use this time to revise concepts, practice coding, and work on your assignments. Make sure to stay productive!",
        "sunday": "Boss, today is a holiday. Take some rest, but also keep an eye on upcoming deadlines and use this time to prepare for the next week!"
    }
    speak(week.get(day, "No schedule available."))

def openApp(command):
    if "calculator" in command:
        speak("Opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("Opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("Opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(command):
    if "calculator" in command:
        speak("Closing calculator")
        os.system("taskkill \\f \\im calc.exe")
    elif "notepad" in command:
        speak("Closing notepad")
        os.system('taskkill \\f \\im notepad.exe')
    elif "paint" in command:
        speak("Closing paint")
        os.system('taskkill \\f \\im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("Boss, what should I search on Google?")
        search_query = command().lower()  # Get search terms from user

        # Validate input and perform the search
        if search_query and search_query != "none":
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            speak("I didn't catch that, please try again.")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage.")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss, our system has {percentage} percentage battery.")
    
    if percentage >= 80:
        speak("Boss, we could have enough charging to continue our recording.")
    elif 40 <= percentage < 75:
        speak("Boss, we should connect our system to a charging point to charge our battery.")
    else:
        speak("Boss, we have very low power, please connect to charging; otherwise, recording should be off.")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who’s afraid of negative numbers? He will stop at nothing to avoid them!",
        "Why was the math book sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    speak(random.choice(jokes))

def get_news():
    API_KEY = "67086616be0e497a8cb28f98a3071bf5"  # Replace with your actual NewsAPI key
    URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'
    response = requests.get(URL)
    articles = response.json().get('articles', [])
    for article in articles[:5]:  # Read top 5 news articles
        speak(f"Title: {article['title']}.")

def get_weather(city="Hyderabad"):
    API_KEY = "f15555f80be535e145ecf4e396e09443"  # Replace with your actual OpenWeatherMap API key
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    data = response.json()
    if data["cod"] == 200:
        main = data['main']
        temperature = main['temp']
        weather_desc = data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {weather_desc}.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")
def about_project():
    """Provide a brief description of the project.This project is an intelligent voice assistant built using Python. """
    description = (
        "This project is an intelligent voice assistant built using Python. "
        "It uses natural language processing to understand commands and provide responses. "
        "The assistant can perform various tasks, such as fetching the latest news, "
        "providing weather updates, managing schedules, and executing simple applications like "
        "calculator and notepad. It can also engage in small talk and tell jokes."
    )
    speak(description)


# Other functions remain the same...
# Include your social_media, schedule, openApp, closeApp, browsing,
# condition, tell_joke, get_news, get_weather, about_project functions here...


if __name__ == "__main__":
    wishMe()
    while True:
        query = command()
        
        # Process commands
        if 'facebook' in query or 'linkedin' in query or 'whatsapp' in query or 'instagram' in query:
            social_media(query)
        elif "university time table" in query or "schedule" in query:
            schedule()
        elif "news" in query or "give me news" in query:
            get_news()
        elif "weather" in query or "what's the weather" in query:
            speak("Please say the city name for the weather.")
            city = command()  # Get city from user
            get_weather(city)
        elif "tell about this project" in query:
            about_project()
        elif "volume up" in query or "increase volume" in query:
            pyautogui.press("volumeup")
            speak("Volume increased.")
        elif "volume down" in query or "decrease volume" in query:
            pyautogui.press("volumedown")
            speak("Volume decreased.")
        elif "volume mute" in query or "mute the sound" in query:
            pyautogui.press("volumemute")
            speak("Volume muted.")
        elif "open calculator" in query or "open notepad" in query or "open paint" in query:
            openApp(query)
        elif "close calculator" in query or "close notepad" in query or "close paint" in query:
            closeApp(query)
        elif "tell me a joke" in query:
            tell_joke()
        elif "what" in query or "who" in query or "how" in query or "hi" in query or "thanks" in query or "hello" in query:
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])
            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        elif "open google" in query or "open edge" in query:
            browsing(query)
        elif "system condition" in query or "condition of the system" in query:
            speak("Checking the system condition.")
            condition()
        elif "exit" in query:
            speak("Goodbye!")
            sys.exit()

        root.update()  # Keeps the tkinter window responsive