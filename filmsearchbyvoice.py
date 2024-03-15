# Install necessary packages
# pip install IMDbPY
# pip install pyttsx3
# pip install SpeechRecognition
# apt-get install -y portaudio19-dev
# pip install sounddevice
# pip install numpy

# Importing required libraries
import imdb
import pyttsx3
import speech_recognition as sr
import datetime
import sounddevice as sd
import numpy as np

# Function for speaking
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)
    engine.say(text)
    engine.runAndWait()

# Function to capture audio from microphone
def get_audio():
    fs = 44100  # Sample rate
    duration = 5  # Duration of recording

    print("Listening... Say something!")

    # Query available input devices
    devices = sd.query_devices()
    print("Available input devices:", devices)

    # Select the appropriate device index for audio input
    input_device_index = None
    for i, device in enumerate(devices):
        if 'input' in device['name'].lower() and 'default' in device['name'].lower():
            input_device_index = i
            break

    if input_device_index is None:
        print("No suitable input device found.")
        return ""

    print("Using input device:", devices[input_device_index]['name'])

    # Record audio using the selected device
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16, device=input_device_index)
    sd.wait()

    # Convert audio to text using SpeechRecognition
    recognizer = sr.Recognizer()
    try:
        # Convert audio to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))
        return ""

# Function for searching movie
def search_movie():
    # gathering information from IMDb
    moviesdb = imdb.IMDb()

    # Search for movie name using captured audio
    text = get_audio()

    print("Searching for:", text)

    # Search for movies using IMDb
    movies = moviesdb.search_movie(text)

    # Handle search results
    if len(movies) == 0:
        speak("No result found")
    else:
        speak("I found these:")

        for movie in movies:
            title = movie['title']
            year = movie['year']

            # Speak the movie title and year
            speak(f'{title}-{year}')

            info = movie.getID()
            movie = moviesdb.get_movie(info)

            title = movie['title']
            year = movie['year']
            rating = movie['rating']
            plot = movie['plot outline']

            # Speak movie details
            if year < int(datetime.datetime.now().strftime("%Y")):
                speak(
                    f'{title} was released in {year} and has an IMDB rating of {rating}. \
                    The plot summary of the movie is {plot}')
            else:
                speak(
                    f'{title} will release in {year} and has an IMDB rating of {rating}. \
                    The plot summary of the movie is {plot}')

# Call the function to start the movie search
search_movie()
