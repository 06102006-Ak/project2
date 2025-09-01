# INDEPENDENT PROJECT -- Voice-Activated Virtual Assistant (Jarvis) OR chatbot assistant named Jarvis

import speech_recognition as sr 
import webbrowser 
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI 
from datetime import datetime

engine = pyttsx3.init() 
# initialized the pyttsx3

def speak(text):
    engine.say(text)
    engine.runAndWait()

chat_history = [
    {"role": "system", "content": "You are a virtual assistant named Jarvis, skilled in general tasks. Keep responses short and helpful."}
]

def aiProcess(command):
    chat_history.append({"role": "user", "content": command})
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        # This is the not OpenAI's stantard API URL, but the Azure OpenAI Service URL which is custom made for Azure.
        # Azure OpenAI Service is a cloud platform from Microsoft that 
        # lets you use OpenAI models (like GPT-4, GPT-4o, etc.) via Azure’s infrastructure instead of OpenAI’s own servers.
        api_key="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",
    )

    response = client.chat.completions.create(
        messages=chat_history,
        model="gpt-4o",
        temperature=1,  # adds the randomness to the response
        max_tokens=4096,  # limit respose length  
        top_p=1
    )
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    return reply

def get_weather_forecast(city):
    api_key = "e08e9cb21160411682b110837250804"  
    base_url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            speak(f"Sorry, I couldn't find weather data for {city}.")
            return

        location = data["location"]["name"]
        region = data["location"]["region"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike = data["current"]["feelslike_c"]
        wind_kph = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]

        weather_report = (
            f"The current weather in {location}, {region} is {condition}. "
            f"Temperature is {temp_c}°C, feels like {feelslike}°C, "
            f"with humidity at {humidity}% and wind speed of {wind_kph} kilometers per hour."
        )

        speak(weather_report)
        print(weather_report)

    except Exception as e:
        speak("Sorry, I couldn't get the weather forecast.")
        print("WeatherAPI error:", e)


def processCommand(c):

#1. Open Command     
    if "open google" == c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open youtube" == c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open iiitr"  == c.lower():
        webbrowser.open("https://iiitr.ac.in/")

#2. Play Command
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        try:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I don't have that song.")

#3. News Command
    elif "news" in c.lower():
        api_key = "91287b72c176497989bf763ef5039a4c"
        query = "technology"
        language = "en"
        url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            for i, article in enumerate(articles[:5], start=1):
                speak(f"{i}. {article['title']}")
        else:
            speak("Failed to fetch news:", response.json())

#4. Weather Command
    elif "weather" in c.lower():
        words = c.lower().split()
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = " ".join(words[city_index:])
                get_weather_forecast(city)
            else:
                speak("Please say the city name after 'in'.")
        else:
            speak("Please say something like 'what's the weather in Raichur'.")

#5. Date and Time Command
    elif "date" in c.lower():
        today = datetime.now().strftime("%A, %d %B %Y")  # e.g., Friday, 08 April 2025
        print(f"Today's date is: {today}")
        speak(f"Today's date is {today}")

    elif "time" in c.lower():
        current_time = datetime.now().strftime("%I:%M %p")  # e.g., 10:30 AM
        print(f"Current time: {current_time}")
        speak(f"The current time is {current_time}")

# Question Command
    else:
        # Let openai handle these command
        output = aiProcess(c)
        print(output)
        speak(output)
        

def listenForCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        speak("Error with speech recognition service.")
        return ""

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    print("Initializing Jarvis...")

    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Say 'Jarvis' to activate...")
            audio = r.listen(source)

        try:
            wake_word = r.recognize_google(audio)
            if wake_word.lower() == "jarvis":
                speak("Jarvis is online.")
                print("Jarvis is online.")
                
                while True:
                    command = listenForCommand()
                    if command.lower() in ["exit", "stop", "shutdown", "bye"]:
                        speak("Goodbye!")
                        print("Session Ended.")
                        exit()
                    elif command:
                        processCommand(command)

        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print("Speech Recognition error:", e)