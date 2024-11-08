import os
import sys

from groq import Groq
import speech_recognition as sr
import pyaudio
import pyttsx3
import datetime
import time
import speedtest
import webbrowser
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from AIUI import Ui_MainWindow



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()



def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak(f"good morning, its {tt}")
    elif hour>12 and hour<18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening,  its {tt}")
    speak("i am jarvis your personal ai assistant,  please tell me,  how can i help you")



os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

system_prompt = {
    "role": "system",
    "content":"You are jarvis my personal ai assisstant and not a language model. You reply with medium answer."

}

chat_history = [system_prompt]


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 3
            audio = r.listen(source, timeout=2, phrase_time_limit=4)

        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:

            return "none"
        return query

    def TaskExecution(self):
        wish()

        while True:

            self.query = self.takecommand()
            if self.query == "none":
                continue
            elif "open google" in self.query:
                speak("what should i search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")
            elif self.query == "check internet speed":
                st = speedtest.Speedtest()
                dl = st.download()
                correctDownload = int(dl / 800000)
                up = st.upload()
                correctupload = int(up / 800000)
                speak(
                    f"sir we have {correctDownload} mega bytes per second downloading speed and {correctupload} mega bytes per second uploading speed")
            elif "quit" in self.query:
                speak("Thank you have a nice day")
                break
            else:
                chat_history.append({"role": "user", "content": self.query})

                response = client.chat.completions.create(model="llama3-70b-8192",
                                                          messages=chat_history,
                                                          max_tokens=1024,
                                                          temperature=1.2)

                chat_history.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                # Print the response
                speak(response.choices[0].message.content)

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie =QtGui.QMovie("image_processing20200211-21870-1d46fyi.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()




app = QApplication(sys.argv)
VA=Main()
VA.show()
exit(app.exec_())
