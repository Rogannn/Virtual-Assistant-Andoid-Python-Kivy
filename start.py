from kivy import Config
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.core.window import Window

from threading import *

import threading
import datetime
import random
import nltk

from recog import sr, speaker
from create_model import MakeVAssistant
from split_words import word_splitter

recognizer = sr.Recognizer()

spoken_list = []

WIDTH = 310
HEIGHT = 580
Window.size = (WIDTH, HEIGHT)
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)

screen_manager = ScreenManager()


class MainApp(MDApp):
    global screen_manager

    stop_event = threading.Event()
    bot_speaking_img = Image(source='images/vaicon-speaking.png')
    bot_idle_img = Image(source='images/vaicon-idle.png')
    bot_listening_img = Image(source='images/vaicon-listening.png')

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

        init_message = "Use your mic or press one of the categories to see answerable questions."
        self.main_screen.ids.user_message_label.text = init_message
        self.main_screen.ids.bot_state_img.source = 'images/vaicon-idle.png'

        return screen_manager

    def download_nltks(self):
        print("0/3")
        self.splash_screen.ids.download_label.text = "0/3"
        nltk.download('punkt')
        print("1/3")
        self.splash_screen.ids.download_label.text = "1/3"
        nltk.download('wordnet')
        print("2/3")
        self.splash_screen.ids.download_label.text = "2/3"
        nltk.download('omw-1.4')
        print("3/3")
        self.splash_screen.ids.download_label.text = "3/3"
        self.loading = False
        Clock.schedule_once(self.change_screen, 1)

    def change_screen(self, dt):
        # change to main screen
        screen_manager.current = "MainScreen"

        t1 = Thread(target=self.init_assistant, args=("Hello",))
        t1.start()

    def on_start(self):
        screen_manager.current = "SplashScreen"
        t2 = Thread(target=self.download_nltks)
        t2.start()

    def set_bot_state(self, state, instance=None, value=None):
        if state == "speaking":
            self.main_screen.ids.bot_state_img.source = 'images/vaicon-speaking.png'
        if state == "listening":
            self.main_screen.ids.bot_state_img.source = 'images/vaicon-listening.png'
        if state == "idle":
            self.main_screen.ids.bot_state_img.source = 'images/vaicon-idle.png'

    def update_user_speech(self, speech):
        self.main_screen.ids.user_message_label.text = speech

    def update_bot_speech(self, speech):
        self.main_screen.ids.bot_message_label.text = speech

    def callback_for_category_items(self, *args):
        query = args[0]
        self.update_user_speech(query)
        t1 = Thread(target=self.init_assistant, args=(query,))
        t1.start()

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
                lambda x, y=item: self.callback_for_category_items(
                    y
                ),
            )
        bottom_sheet_menu.open()

    spoken_list = []

    def aiResponse(self, response):
        global recognizer
        text = word_splitter(response)
        spoken_list.append(response)
        self.update_bot_speech(text)
        print("Spoken List: " + str(spoken_list))

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
        assistant.request(text)
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
                assistant.request(message)
            except sr.UnknownValueError:
                recognizer = sr.Recognizer()
            if self.stop_event.is_set():
                break

    def on_stop(self):
        self.stop_event.set()


main = MainApp()


# RESPONSES SETUP
def hello():
    choices = ["Greetings, what would you like to ask?",
               "Hi, what would you like to ask?",
               "Hello, what would you like to ask?"]
    chosen_statement = random.choice(choices)
    main.aiResponse(chosen_statement)


def current_date():
    d = datetime.datetime.now().strftime('%B %d, %Y')
    response = "Today is " + d
    main.aiResponse(response)


def howisit():
    choices = ["I'm good, thank you for asking",
               "I am working fine, thank you for asking"]
    chosen_statement = random.choice(choices)
    main.aiResponse(chosen_statement)


def timeCheck():
    time = datetime.datetime.now().strftime('%I:%M %p')
    response = "The current time is " + time
    main.aiResponse(response)


def gratitude():
    choices = ["Your welcome",
               "No problem"]
    chosen_statement = random.choice(choices)
    main.aiResponse(chosen_statement)


def courses():
    main.aiResponse("AVAILABLE COURSES IN DHVSU PORAC CAMPUS| "
                    "Bachelor of Elementary Education Major in General Education.| "
                    "Bachelor of Science in Business Administration Major in Marketing.| "
                    "Bachelor of Science in Information Technology.| "
                    "Bachelor of Science in Social Work")


def register():
    main.aiResponse(
        "To register, go to the registrar of the school. You can then ask more questions to the person assigned there.")


def enrollment():
    main.aiResponse(
        "To enroll, you can go to the Administrative room. You can then ask the person in charge for further inquiries.")


def teachersToAsk():
    main.aiResponse(
        "You can go to the Faculty room of the school to see the teachers or you can go to their own office.")


def tuition_fee_per_sem():
    main.aiResponse(
        "Under the Law students in accredited State and Local universities/colleges will not pay any tuition "
        "fees or misc fee.")


def uni_mission():
    main.aiResponse("DHVSU MISSION:| "
                    "DHVSU commits itself to provide an environment conducive to continuous creation of knowledge and "
                    "technology towards the transformation of students into globally competitive professionals "
                    "through the synergy of appropriate teaching, research, service and productivity functions.")


def uni_vision():
    main.aiResponse("DHVSU VISION:| "
                    "A lead university in producing quality individuals with competent capacities to generate "
                    "knowledge and technology and enhance professional practices for sustainable national and global "
                    "competitiveness through continuous innovation.")


def director_of_campus():
    main.aiResponse("DENNIS V. DIZON, M.A.Ed. is the Campus Director of DHVSU Porac Campus")


def academic_cp_of_campus():
    main.aiResponse("Aileen L. Koh, M.A.Ed. is the Academic Chairperson of DHVSU Porac Campus")


def requirements_to_enroll():
    main.aiResponse("Requirements for freshmen to enroll in DHVSU Porac Campus:| "
                    "A Duly accomplished Application Form Photocopy of Form138,| "
                    "2 pieces passport size picture with name tag (white background),| "
                    "and a PSA Birth Certificate")


def requirements_of_transferees():
    main.aiResponse("Requirements for transferees to enroll in DHVSU Porac Campus:| "
                    "1. Duly accomplished Application Form Photocopy of Grades Copy of Honorable Dismissal "
                    "Certificate of Good Moral| 2. 2 pcs. passport size picture with name tag (white background)")


def location_of_campus():
    main.aiResponse(
        "The DHVSU Porac Campus is located in Porac, Pampanga, and is 15.06 kilometers away, west of the main "
        "campus of DHVSU in Bacolor, Pampanga.")


def public_or_private_uni():
    main.aiResponse("Don Honorio Ventura State University is a PUBLIC university.")


def exitApp():
    choices = ["Have a nice day!",
               "Good bye!",
               "See you soon!"]
    chosen_statement = random.choice(choices)
    main.aiResponse(chosen_statement)


def replay_speech():
    li = len(spoken_list) - 1
    speech = spoken_list[li]
    print("Repeating: " + speech)
    main.aiResponse(speech)


mappings = {
    "tuition_fee_per_sem": tuition_fee_per_sem,
    "to_register": register,
    "to_enroll": enrollment,
    "ask_teacher": teachersToAsk,
    "greeting": hello,
    "gratitude": gratitude,
    "howisit": howisit,
    "time_check": timeCheck,
    "exit": exitApp,
    "available_courses": courses,
    "current_date": current_date,
    "replay": replay_speech,
    "uni_mission": uni_mission,
    "uni_vision": uni_vision,
    "director_of_campus": director_of_campus,
    "academic_cp_of_campus": academic_cp_of_campus,
    "requirements_to_enroll": requirements_to_enroll,
    "requirements_of_transferees": requirements_of_transferees,
    "public_or_private_uni": public_or_private_uni,
    "location_of_campus": location_of_campus
}

assistant = MakeVAssistant('intents.json', intent_methods=mappings)
assistant.load_model()

main.run()
