import speech_recognition as aa
import pyttsx3 
import pywhatkit
import datetime
import wikipedia
#import threading

listner = aa.Recognizer()

#machine = pyttsx3.init()
def talk(text):
    print("Friday speaking:", text)
    machine = pyttsx3.init()
    machine.say(text)
    machine.runAndWait()
    machine.stop()
    


def input_instruction():
    global instruction
    try:
        with aa.Microphone(device_index=2) as origin:
            print(" Hey, I am Friday , whats your name?")
            talk('Hey, I am Friday , whats your name?')

            listner.adjust_for_ambient_noise(origin, duration=0.5)
            print("listening...")
            speech = listner.listen(origin, timeout=5, phrase_time_limit=10)

            ''' # Save audio for debugging
            with open("debug.wav", "wb") as f:
                f.write(speech.get_wav_data())
            print("Audio saved as debug.wav")'''

            print("listening complete")
            instruction = listner.recognize_google(speech)
            print("Recognition complete")
            instruction = instruction.lower()
            print("Recognized instruction:" ,instruction)

            if "faizal" in instruction or "faisal" in instruction:
                play_Friday()
            elif "how are you" in instruction or "how r u" in instruction:
                talk("I am fine, what about you?")
                play_Friday()
            else:
                talk("Say correct name")

    except aa.UnknownValueError:
        print("Could not understand audio")
    except aa.RequestError:
        print("Could not get results from Google API")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
def play_Friday():
    print("yes faizal what can I do for you today")
    talk('yes faizal what can I do for you today')
    
    import time
    time.sleep(0.5)  # Bolne ke baad mic thoda wait

    while True:
        try:
            with aa.Microphone(device_index=2) as origin:
                listner.adjust_for_ambient_noise(origin, duration=0.5)
                print("listening...")
                speech = listner.listen(origin, timeout=10, phrase_time_limit=20)
                print("listening complete")

            instruction = listner.recognize_google(speech).lower()
            print("Recognized instruction:", instruction)

            if "play" in instruction:
                song = instruction.replace('play',"").strip()
                talk("playing " + song)
                pywhatkit.playonyt(song)
                break

            elif "time" in instruction:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time ' + time)
                print("current time:", time)

            elif "date" in instruction:
                date = datetime.datetime.now().strftime('%d/%m/%y')
                talk("Today's date " + date)
                print("today's date:", date)

            elif "who is" in instruction:
                human = instruction.replace('who is',"").strip()
                info = wikipedia.summary(human, 1)
                print(info)
                talk(info)

            elif "exit" in instruction or "quit" in instruction:
                talk("Goodbye Faizal! See you soon.")
                break

            else:
                talk('please repeat')

        except aa.UnknownValueError:
            talk("Sorry, I didn’t catch that.")
        except aa.RequestError:
            talk("Google API error, please check your connection.")
        except Exception as e:
            print("Error:", e)
            talk("Something went wrong.")


input_instruction()