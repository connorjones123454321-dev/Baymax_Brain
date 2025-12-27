# ==============================
# BAYMAX OS
# Movie-Style Healthcare Companion
# ==============================

import time
import random
import pyttsx3
import speech_recognition as sr

# GPIO is optional if not on Raspberry Pi
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# ==============================
# TEXT TO SPEECH (BAYMAX VOICE)
# ==============================
engine = pyttsx3.init()
engine.setProperty('rate', 120)      # Slow, calm speech
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Calm male voice (change if needed)

def speak(text):
    print("Baymax:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.6)  # Movie-like pause

# ==============================
# VOICE RECOGNITION
# ==============================
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen(prompt=None, timeout=6):
    if prompt:
        speak(prompt)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio)
            print("User:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            speak("I did not hear anything.")
        except sr.UnknownValueError:
            speak("I could not understand you.")
        except sr.RequestError:
            speak("There was a connection error.")
    return ""

# ==============================
# GPIO / SAFETY (OPTIONAL)
# ==============================
if GPIO_AVAILABLE:
    HEART_SENSOR_PIN = 17
    PRESSURE_SENSOR_PIN = 27
    EMERGENCY_STOP_PIN = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HEART_SENSOR_PIN, GPIO.IN)
    GPIO.setup(PRESSURE_SENSOR_PIN, GPIO.IN)
    GPIO.setup(EMERGENCY_STOP_PIN, GPIO.IN)

def check_safety():
    if GPIO_AVAILABLE:
        if GPIO.input(EMERGENCY_STOP_PIN):
            speak("Emergency detected. Shutting down.")
            GPIO.cleanup()
            exit()

def read_sensors():
    if GPIO_AVAILABLE:
        return {
            "heart_rate": GPIO.input(HEART_SENSOR_PIN),
            "pressure": GPIO.input(PRESSURE_SENSOR_PIN)
        }
    return {}

# ==============================
# MOVEMENT PLACEHOLDERS
# ==============================
def move_arm(position):
    print(f"[MOVEMENT] Arm to {position} degrees")
    # Servo control goes here

def wave_hand():
    for pos in [0, 45, 0, 45, 0]:
        move_arm(pos)
        time.sleep(0.5)

# ==============================
# PERSONALITY LOGIC
# ==============================
def ask_how_are_you():
    speak("Hello. I am Baymax, your personal healthcare companion.")

    response = listen("On a scale of one to ten, how would you rate your day?")
    
    rating = None
    for word in response.split():
        if word.isdigit():
            rating = int(word)
            break

    if rating is None:
        rating = random.randint(1, 10)

    speak(f"You rated your day a {rating}.")

    if rating <= 3:
        speak("I am concerned. Please take care of yourself.")
    elif rating <= 7:
        speak("I see. Please remember to rest when needed.")
    else:
        speak("That is excellent. Continue your positive behavior.")

# ==============================
# DEACTIVATION LOGIC (ICONIC)
# ==============================
def deactivate_baymax():
    speak("I cannot deactivate until you are satisfied with my care.")

    satisfied = False
    while not satisfied:
        response = listen("Are you satisfied with your care?")

        if any(phrase in response for phrase in [
            "yes", "satisfied", "i am satisfied"
        ]):
            satisfied = True
            speak("Thank you. I will now deactivate.")
        else:
            speak("I am here to continue your care.")

# ==============================
# MAIN LOOP
# ==============================
def main():
    speak("System check complete. Baymax is operational.")

    try:
        while True:
            check_safety()
            read_sensors()
            ask_how_are_you()
            wave_hand()
            time.sleep(10)

    except KeyboardInterrupt:
        deactivate_baymax()
        if GPIO_AVAILABLE:
            GPIO.cleanup()

# ==============================
# START BAYMAX
# ==============================
if __name__ == "__main__":
    main()
