from googletrans import Translator
from googletrans.constants import LANGCODES
from gtts import gTTS
import os 
import pyperclip
import speech_recognition as sr
import pygame
import time
from mutagen.mp3 import MP3

def play_back_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def speech_to_text():
    required=0
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            required= index
    r = sr.Recognizer()
    with sr.Microphone(device_index=required) as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=4)
    try:
        input = r.recognize_google(audio)
        print("You said: " + input)
        return str(input)
    except sr.UnknownValueError:
        print("Sorry I Didn't Get that!!")
        text_to_speech("Sorry I Didn't Get that!!","en")
        play_back_music("output.mp3")
        time.sleep(3)
        os.remove("output.mp3")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def text_to_speech(myText,language):
    output = gTTS(text=myText, lang=language, slow = False)
    output.save("output.mp3")

def repeat_sound(myText,language):
    output = gTTS(text=myText, lang=language, slow = False)
    output.save("repeat.mp3")

def transl():
    text_to_speech("enter the language :","en")
    play_back_music("output.mp3")
    LANG = input("enter the language :").lower()
    lang = LANGCODES[LANG]
    os.remove("output.mp3")
    inp = speech_to_text()
    translater = Translator()
    filePath = 'rishabhbilwal/translator/output.mp3'
    
    if inp is not None:
        out = translater.translate(inp, dest=lang)
        say = out.text
        print(say)
        text_to_speech("do you want to copy text to clipboard ?","en")
        play_back_music("output.mp3")
        cp = input("do you want to copy text to clipboard ?")
        os.remove("output.mp3")
        if cp == 'yes':
            pyperclip.copy(say)
            spam = pyperclip.paste()

        text_to_speech("do you want us to pronounce?","en")
        play_back_music("output.mp3")
        a = input("do you want us to pronounce?")
        os.remove("output.mp3")
        if a == 'yes':
            myText = say
            language = lang
            text_to_speech(myText,language)
            play_back_music("output.mp3")
            audio = MP3("output.mp3")
            audio_info = audio.info
            length_in_secs = int(audio_info.length)

            while True:
                time.sleep(length_in_secs+1)
                repeat_sound("do you want us to repeat ? ","en")
                play_back_music("repeat.mp3")
                user = input("do you want us to repeat ? ")
                if user == "yes":
                    os.remove("repeat.mp3")
                    play_back_music("output.mp3")
                else:
                    os.remove("output.mp3")
                    os.remove("repeat.mp3")
                    if os.path.exists(filePath):
                        os.remove(filePath)
                    break

        elif a is not None:
            if os.path.exists(filePath):
                os.remove(filePath)
            else:
                print("Can not delete the file as it doesn't exists")
    
    text_to_speech("do you want to continue ?","en")
    play_back_music("output.mp3")
    cont = input("do you want to continue ?")
    os.remove("output.mp3")
    if cont == "yes":
        transl()

if __name__ == "__main__":
    pygame.mixer.init()
    try:
        transl()
    except:
        print("-"*50)
        print("oops seems there's no internet connection..!!")
        print("-"*50)

            

