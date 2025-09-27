import speech_recognition as aa
import pickle, wikipedia, datetime, pywhatkit, os
import pyttsx3

listner = aa.Recognizer()
reminder_file = "reminders.txt"

# Load trained intent model
with open("intent_model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

# Text-to-speech function
def talk(text):
    print("Friday:", text)
    machine = pyttsx3.init()
    machine.say(text)
    machine.runAndWait()
    machine.stop()

# Predict intent from user text
def get_intent(user_text, threshold=0.5):
    X = vectorizer.transform([user_text])
    probs = model.predict_proba(X)[0]
    predicted_intent = model.classes_[probs.argmax()]
    confidence = probs.max()
    if confidence < threshold:
        return "unknown"
    return predicted_intent

# Auto-generate new intent names
def generate_intent_name(user_text):
    words = user_text.lower().split()
    verbs = ["play", "set", "open", "send", "remind", "create", "tell"]
    nouns = ["music", "reminder", "alarm", "email", "note", "timer"]

    chosen_verb = next((w for w in words if w in verbs), None)
    chosen_noun = next((w for w in words if w in nouns), None)

    if chosen_verb and chosen_noun:
        return f"{chosen_verb}_{chosen_noun}"
    elif chosen_verb:
        return f"{chosen_verb}_action"
    elif chosen_noun:
        return f"{chosen_noun}_action"
    else:
        return "_".join(words[:2])  # fallback

# Save reminder only 
def set_reminder(time_str, message):
    with open(reminder_file, "a") as f:
        f.write(f"{time_str}|||{message}\n")
    talk(f"Reminder saved for {time_str}: {message}")

# Perform action based on intent
def play_Friday(user_text):
    intent = get_intent(user_text, threshold=0.2)
    print("Predicted intent:", intent)

    if intent == "play_music":
        song = user_text.replace("play", "").strip()
        talk("Playing " + song)
        pywhatkit.playonyt(song)
        
    elif intent == "get_time":
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk("Current time is " + time)

    elif intent == "get_date":
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + date)

    elif intent == "ask_person":
        person = user_text.replace("who is", "").strip()
        info = wikipedia.summary(person, 1)
        talk(info)

    elif intent == "greet":
        talk("I am fine, what can I do for you?")

    elif intent == "exit":
        talk("Goodbye Buddy!")
        exit()

    # Handle saving reminders
    elif "set reminder" in user_text:
        try:
            parts = user_text.split("for")
            msg = parts[0].replace("set reminder", "").strip()
            time_part = parts[1].strip()  # Example: "17:00"
            set_reminder(time_part, msg if msg else "No message")
        except:
            talk("Sorry, I could not understand the reminder format. Please say like 'set reminder go for walk for 17:00'.")

    else:
        # Unknown intent → ask user
        suggested_intent = generate_intent_name(user_text)
        talk(f"I think this command is about '{suggested_intent}'. Say 'yes', 'no', or 'skip'.")

        response = input_instruction(return_only=True, timeout=3, phrase_time_limit=3)

        if response and "yes" in response:
            chosen_intent = suggested_intent
            with open("new_data.txt", "a") as f:
                f.write(f"{user_text}|||{chosen_intent}\n")
            talk(f"Got it! I will remember this command as {chosen_intent}.")

        elif response and "no" in response:
            talk("Okay, please say the correct intent.")
            correction = input_instruction(return_only=True, timeout=4, phrase_time_limit=4)
            if correction:
                chosen_intent = correction.replace(" ", "_")
                with open("new_data.txt", "a") as f:
                    f.write(f"{user_text}|||{chosen_intent}\n")
                talk(f"Thanks! I will remember this as {chosen_intent}.")
            else:
                talk("Didn't catch correction, skipping.")

        else:  # skip or silence
            talk("Skipping intent learning. Let's continue.")

# Listen for input
def input_instruction(return_only=False, timeout=3, phrase_time_limit=5):
    try:
        with aa.Microphone(device_index=2) as origin:
            print("Listening...")
            listner.adjust_for_ambient_noise(origin, duration=0.5)
            speech = listner.listen(origin, timeout=timeout, phrase_time_limit=phrase_time_limit)
            instruction = listner.recognize_google(speech).lower().strip()
            print("Recognized instruction:", instruction)

            if return_only:
                return instruction   # just return text (for yes/no/skip etc.)
            else:
                play_Friday(instruction)

    except aa.UnknownValueError:
        print("Could not understand audio")
        return None
    except aa.RequestError:
        print("Could not get results from Google API")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

talk("Hello!! I am Friday, What can I do for you?")
while True:
    input_instruction()
