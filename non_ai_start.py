import re

from kivy import Config
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.core.window import Window

from threading import *

import threading
import datetime
import random
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem

from recog import sr, speaker
from split_words import word_splitter
from queries import *

recognizer = sr.Recognizer()

spoken_list = []

screen_manager = ScreenManager()


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class MainApp(MDApp):
    global screen_manager
    dialog = None

    stop_event = threading.Event()
    bot_speaking_img = Image(source='vaicon-speaking.png')
    bot_idle_img = Image(source='vaicon-idle.png')
    bot_listening_img = Image(source='vaicon-listening.png')

    def __init__(self, **kwargs):
        super().__init__()
        self.main_screen = None
        self.splash_screen = None
        self.loading = True

    def build(self):
        print("building..")
        self.title = "Virtual Assistant Mobile"
        self.splash_screen = Builder.load_file("splashScreen.kv")
        self.main_screen = Builder.load_file("mainScreen.kv")
        screen_manager.add_widget(self.splash_screen)
        screen_manager.add_widget(self.main_screen)

        init_message = "Use your mic and speak! See available questions."
        self.main_screen.ids.user_message_label.text = init_message
        self.main_screen.ids.bot_state_img.source = 'vaicon-idle.png'

        return screen_manager

    def change_screen(self, dt):
        # change to main screen
        screen_manager.current = "MainScreen"

        t1 = Thread(target=self.init_assistant, args=("Hello",))
        t1.start()

    def on_start(self):
        screen_manager.current = "SplashScreen"
        Clock.schedule_once(self.change_screen, 3)

    def set_bot_state(self, state, instance=None, value=None):
        if state == "speaking":
            self.main_screen.ids.bot_state_img.source = 'vaicon-speaking.png'
        if state == "listening":
            self.main_screen.ids.bot_state_img.source = 'vaicon-listening.png'
        if state == "idle":
            self.main_screen.ids.bot_state_img.source = 'vaicon-idle.png'

    def update_user_speech(self, speech):
        self.main_screen.ids.user_message_label.text = speech

    def update_bot_speech(self, speech):
        self.main_screen.ids.bot_message_label.text = speech

    def callback_for_category_items(self, *args):
        query = args[0]
        self.update_user_speech(query)
        self.show_question_dialog(query)
        self.dialog.title = query

    def show_question_dialog(self, query):
        if not self.dialog:
            self.dialog = MDDialog(
                title=query,
                type="simple",
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dialog_close
                    )
                ],
            )
        self.dialog.open()

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def show_category_data(self, category):
        queries = {
            1: ["What are the requirements of Freshmen to enroll in DHVSU Porac Campus?",
                "What courses are available at DHVSU Porac Campus?",
                "What are the requirements of Transferees to enroll in DHVSU Porac Campus?"],
            2: ["How much is the tuition fee per semester?",
                "Where is DHVSU Porac Campus Located?",
                "Is DHVSU public or private?"],
            3: ["Who is the Director at DHVSU Porac Campus?",
                "Who is the Academic Chairperson at DHVSU Porac Campus?",
                "What is the DHVSU Mission?",
                "What is the DHVSU Vision?"]
        }
        bottom_sheet_menu = MDListBottomSheet()
        for item in queries[category]:
            bottom_sheet_menu.add_item(
                item,
                lambda x, y=item: self.callback_for_category_items(y),
            )
        bottom_sheet_menu.open()

    spoken_list = []

    def aiResponse(self, received_query):
        lower = received_query.casefold()
        remove_whitespaces = lower.strip()
        query = re.sub(r'[^\w]', ' ', remove_whitespaces)
        print(query)

        if requirements_to_enroll.find(query) != -1:
            response = "Requirements for freshmen to enroll in DHVSU Porac Campus:| A Duly accomplished Application " \
                       "Form Photocopy of Form138,| 2 pieces passport size picture with name tag (white background)," \
                       "| and a PSA Birth Certificate "
            self.speak(response)
        elif public_or_private_uni.find(query) != -1:
            response = "Don Honorio Ventura State University is a PUBLIC university."
            self.speak(response)
        elif location_of_campus.find(query) != -1:
            response = "The DHVSU Porac Campus is located in Porac, Pampanga, and is 15.06 kilometers away, " \
                       "west of the main campus of DHVSU in Bacolor, Pampanga."
            self.speak(response)
        elif requirements_of_transferees.find(query) != -1:
            response = "Requirements for transferees to enroll in DHVSU Porac Campus:| " \
                       "1. Duly accomplished Application Form Photocopy of Grades Copy of Honorable Dismissal " \
                       "Certificate of Good Moral| 2. 2 pcs. passport size picture with name tag (white background)"
            self.speak(response)
        elif academic_cp_of_campus.find(query) != -1:
            response = "Aileen L. Koh, M.A.Ed. is the Academic Chairperson of DHVSU Porac Campus."
            self.speak(response)
        elif director_of_campus.find(query) != -1:
            response = "DENNIS V. DIZON, M.A.Ed. is the Campus Director of DHVSU Porac Campus."
            self.speak(response)
        elif uni_mission.find(query) != -1:
            response = "DHVSU MISSION:| " \
                       "DHVSU commits itself to provide an environment conducive to continuous creation of knowledge " \
                       "and technology towards the transformation of students into globally competitive professionals " \
                       "through the synergy of appropriate teaching, research, service and productivity functions."
            self.speak(response)
        elif uni_vision.find(query) != -1:
            response = "DHVSU VISION:| " \
                       "A lead university in producing quality individuals with competent capacities to generate " \
                       "knowledge and technology and enhance professional practices for sustainable national and " \
                       "global competitiveness through continuous innovation."
            self.speak(response)
        elif tuition_fee_per_sem.find(query) != -1:
            response = "Under the Law students in accredited State and Local universities/colleges will not pay any " \
                       "tuition fees or misc fee. "
            self.speak(response)
        elif available_courses.find(query) != -1:
            response = "AVAILABLE COURSES IN DHVSU PORAC CAMPUS| " \
                       "Bachelor of Elementary Education Major in General Education.| " \
                       "Bachelor of Science in Business Administration Major in Marketing.| " \
                       "Bachelor of Science in Information Technology.| " \
                       "Bachelor of Science in Social Work"
            self.speak(response)
        elif replay.find(query) != -1:
            li = len(spoken_list) - 1
            speech = spoken_list[li]
            response = speech
            self.speak(response)
        elif to_register.find(query) != -1:
            response = "To register, go to the registrar of the school. You can then ask more questions to the person " \
                       "assigned there. "
            self.speak(response)
        elif howisit.find(query) != -1:
            choices = ["I'm good, thank you for asking",
                       "I am working fine, thank you for asking"]
            response = random.choice(choices)
            self.speak(response)
        elif time_check.find(query) != -1:
            time = datetime.datetime.now().strftime('%I:%M %p')
            response = "The current time is " + time
            self.speak(response)
        elif gratitude.find(query) != -1:
            choices = ["Your welcome",
                       "No problem"]
            response = random.choice(choices)
            self.speak(response)
        elif exit.find(query) != -1:
            choices = ["Have a nice day!",
                       "Good bye!",
                       "See you soon!"]
            response = random.choice(choices)
            self.speak(response)
        elif current_date.find(query) != -1:
            d = datetime.datetime.now().strftime('%B %d, %Y')
            response = "Today is " + d
            self.speak(response)
        elif greeting.find(query) != -1:
            choices = ["Greetings, what would you like to ask?",
                       "Hi, what would you like to ask?",
                       "Hello, what would you like to ask?"]
            response = random.choice(choices)
            self.speak(response)
        else:
            response = "I'm sorry, it seems that your query is not on my database yet."
            self.speak(response)

    def speak(self, response):
        global recognizer
        text = word_splitter(response)
        spoken_list.append(response)
        self.update_bot_speech(text)

        try:
            self.set_bot_state("speaking")
            speaker.say(response)
            speaker.runAndWait()
        except RuntimeError:
            recognizer = sr.Recognizer()
            print("RuntimeError, already speaking!")
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            print("There was a problem in receiving the words of the speaker, the words might be too unrecognizable.")

        self.set_bot_state("idle")

    def init_assistant(self, text):
        global recognizer
        self.aiResponse(text)
        while True:
            print("listening..")
            self.set_bot_state("idle")
            try:
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=1)
                    audio = recognizer.listen(mic)

                    energy_threshold = recognizer.energy_threshold
                    print("energy_threshold: " + str(energy_threshold))
                    if energy_threshold > 100:
                        self.set_bot_state("listening")

                    message = recognizer.recognize_google(audio)
                    message = message.lower()
                self.update_user_speech(message)
                self.aiResponse(message)
            except sr.UnknownValueError:
                recognizer = sr.Recognizer()
            if self.stop_event.is_set():
                break

    def on_stop(self):
        self.stop_event.set()


main = MainApp()
main.run()
