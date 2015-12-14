#!/usr/bin/env python3
import unicodedata
import re
import os
import sys
import subprocess as sub
import speech_recognition as sr
import codecs
import numpy as np

# recognize speech using Google Speech Recognition
chars = (chr(i) for i in range(0x110000))
control_chars = ''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_chars(f):

    return control_char_re.sub('', f)

def say(msg=None, rate="120", voice="Oliver", f=None):

    if msg is None and f:
        print("msg: {}, rate: {}, voice: {}, file: {}".format(msg, rate, voice, f))
        print("msg: {}, rate: {}, voice: {}, file: {}".format(type(msg), type(rate), type(voice), type(f)))

        sub.Popen(["say", "-r", str(rate), "-v", str(voice), "-f", str(f)])

    elif msg is '':
        return

    if f is None:
        sub.Popen(["say", "-r", str(rate), "-v", str(voice), msg])

def lewis(length, primetext=None):
    
    randyear = np.random.randint(1, 5)
    years = ["one million", "ten thousand", "one thousand", "one hundred",
             "two hundred"]
    if primetext is None:
        primetext = years[randyear]
    print (primetext)
    length = str(length)
    print (type(primetext), type(length))
    os.system("th generate.lua cv/lm_lstm_epoch17.15_1.2414.t7 -gpuid -1 -length {} -primetext \"{}\"".format(length, primetext))
    with open("story.txt", "rb") as f:
        lines = f.read()
        ulines = codecs.decode(lines, 'utf-8', errors='replace')

    with open("utf.txt", "wb") as story:
        story.write(bytes(ulines, 'utf-8'))

while (1) :
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)


    try:
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        word = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


    if word == "tell me a story":
        lewis(2000, None)
        say(f="utf.txt")

    if word == "who are you":
        say("this is oliver, of course", 120, "oliver")

    if word == "my day is ok how is yours":
        say("I'm stuck in this box", 120, "oliver")
    if "scan" in word:
        say("scanning for intent now", 120, "oliver")
        lewis(50, "no hostile intentions ")
        word = None
        #opencv.scan(/Applications/vlc)
        #feed = webcam 
        #object label

