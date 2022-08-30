from kivy.lang import Builder

from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.uix.image import Image
from kivymd.app import MDApp

from threading import *

import threading

from recog import sr
from responses import assistant

recognizer = sr.Recognizer()

KV = '''
MDScreen:

    canvas.before:
        Color:
            rgba: ((217/255,187/255,142/255,1))
        Rectangle:
            pos: self.pos
            size: self.size

    MDTopAppBar:
        id: top_bar
        pos_hint: {"top": 1}
        title: "Virtual Assistant Support in DHVSU Porac Campus Application"
    
    BoxLayout:
        pos: 0, 430
        Image:
            width: 100
            size_hint_y: None
            allow_stretch: True
            source: "images/vaicon-idle.png"
    
    BoxLayout:
        size_hint_y: None
        pos: 0, 250
        Label:
            text: "Available Questions:"
            font_size: 20
            color: 0,0,0,1

    MDRaisedButton:
        text: "Category 1"
        on_release: app.show_category_data(1)
        pos_hint: {"center_x": .5, "center_y": .430}
        md_bg_color: ((228/255,118/255,93/255,1))
        line_color: 1, 1, 1, 1
        elevation: 20

    MDRaisedButton:
        text: "Category 2"
        on_release: app.show_category_data(2)
        pos_hint: {"center_x": .5, "center_y": .365}
        md_bg_color: ((228/255,118/255,93/255,1))
        line_color: 1, 1, 1, 1
        elevation: 20

    MDRaisedButton:
        text: "Category 3"
        on_release: app.show_category_data(3)
        pos_hint: {"center_x": .5, "center_y": .30}
        md_bg_color: ((228/255,118/255,93/255,1))
        line_color: 1, 1, 1, 1
        elevation: 20
    
    BoxLayout:
        size_hint_y: None
        height: user_message_label.height
        pos: 0, 50
        Label:
            id: user_message_label 
            text: " "
            font_size: 15
            color: 0,0,0,1
            size_hint: 1, None
            markup: True
            halign: "center"
            size: self.texture_size
            pos_hint:{"x":.18, "y":.8}
            background_color: 1,1,1,1
            canvas.before:
                Color:
                    rgba: self.background_color
                Rectangle:
                    pos: self.pos
                    size: self.size
    BoxLayout:
        size_hint_y: None
        height: bot_message_label.height
        pos: 0, 400
        padding: 50
        Label:
            id: bot_message_label 
            text: "Greetings."
            font_size: 20
            color: 0,0,0,1
            size_hint: 1, None
            markup: True
            halign: "center"
            size: self.texture_size
            pos_hint:{"center_x":.5, "center_y":.5}
            background_color: 1,1,1,1
            canvas.before:
                Color:
                    rgba: self.background_color
                Rectangle:
                    pos: self.pos
                    size: self.size
'''


class MainApp(MDApp):
    bot_img = Image(source='images/vaicon-idle.png')
    stop_event = threading.Event()

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        init_message = self.word_splitter("Use your mic or press one of the categories to see answerable questions.")
        self.root.ids.user_message_label.text = init_message
        t1 = Thread(target=self.init_assistant, args=("hello",))
        t1.start()

    def word_splitter(self, words):
        word_limit = 6
        split_words = words.split()
        new_text = ""
        word_count = 0
        for word in split_words:
            new_text += word + " "
            word_count += 1
            if word_count > word_limit or "|" in word:
                new_text += "\n"
                word_count = 0
        return new_text.replace("|", "")

    def change_bot_state(self, instance=None, value=None):
        self.bot_img.source = 'vaicon-speaking.png'

    def update_user_speech(self, speech):
        user_message = self.word_splitter(speech)
        self.root.ids.user_message_label.text = user_message

    def update_bot_speech(self, speech):
        bot_message = self.word_splitter(speech)
        self.root.ids.bot_message_label.text = bot_message

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

    def init_assistant(self, text):
        global recognizer
        assistant.request(text)
        while True:
            print("listening..")
            # bot_state.idle(window, bot_idle)
            try:
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=1)
                    audio = recognizer.listen(mic)

                    energy_threshold = recognizer.energy_threshold
                    print("energy_threshold: " + str(energy_threshold))
                    # if energy_threshold > 100:
                    #     bot_state.listening(window, bot_listening)

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


MainApp().run()
