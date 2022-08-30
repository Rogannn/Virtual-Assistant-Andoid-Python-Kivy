from create_model import MakeVAssistant
from ai_response import aiResponse, spoken_list

import datetime
import random


# RESPONSES SETUP
def hello():
    choices = ["Greetings, what would you like to ask?",
               "Hi, what would you like to ask?",
               "Hello, what would you like to ask?"]
    chosen_statement = random.choice(choices)
    aiResponse(chosen_statement)


def current_date():
    d = datetime.datetime.now().strftime('%B %d, %Y')
    response = "Today is " + d
    aiResponse(response)


def howisit():
    choices = ["I'm good, thank you for asking",
               "I am working fine, thank you for asking"]
    chosen_statement = random.choice(choices)
    aiResponse(chosen_statement)


def timeCheck():
    time = datetime.datetime.now().strftime('%I:%M %p')
    response = "The current time is " + time
    aiResponse(response)


def gratitude():
    choices = ["Your welcome",
               "No problem"]
    chosen_statement = random.choice(choices)
    aiResponse(chosen_statement)


def courses():
    aiResponse("AVAILABLE COURSES IN DHVSU PORAC CAMPUS| "
               "Bachelor of Elementary Education Major in General Education.| "
               "Bachelor of Science in Business Administration Major in Marketing.| "
               "Bachelor of Science in Information Technology.| "
               "Bachelor of Science in Social Work")


def register():
    aiResponse(
        "To register, go to the registrar of the school. You can then ask more questions to the person assigned there.")


def enrollment():
    aiResponse(
        "To enroll, you can go to the Administrative room. You can then ask the person in charge for further inquiries.")


def teachersToAsk():
    aiResponse(
        "You can go to the Faculty room of the school to see the teachers or you can go to their own office.")


def tuition_fee_per_sem():
    aiResponse(
        "Under the Law students in accredited State and Local universities/colleges will not pay any tuition "
        "fees or misc fee.")


def uni_mission():
    aiResponse("DHVSU MISSION:| "
               "DHVSU commits itself to provide an environment conducive to continuous creation of knowledge and "
               "technology towards the transformation of students into globally competitive professionals through the "
               "synergy of appropriate teaching, research, service and productivity functions.")


def uni_vision():
    aiResponse("DHVSU VISION:| "
               "A lead university in producing quality individuals with competent capacities to generate knowledge "
               "and technology and enhance professional practices for sustainable national and global competitiveness "
               "through continuous innovation.")


def director_of_campus():
    aiResponse("DENNIS V. DIZON, M.A.Ed. is the Campus Director of DHVSU Porac Campus")


def academic_cp_of_campus():
    aiResponse("Aileen L. Koh, M.A.Ed. is the Academic Chairperson of DHVSU Porac Campus")


def requirements_to_enroll():
    aiResponse("Requirements for freshmen to enroll in DHVSU Porac Campus:| "
               "1. Duly accomplished Application Form Photocopy of Form138| "
               "2. 2 pcs. passport size picture with name tag (white background)| "
               "3. PSA Birth Certificate")


def requirements_of_transferees():
    aiResponse("Requirements for transferees to enroll in DHVSU Porac Campus:| "
               "1. Duly accomplished Application Form Photocopy of Grades Copy of Honorable Dismissal Certificate of "
               "Good Moral| "
               "2. 2 pcs. passport size picture with name tag (white background)")


def location_of_campus():
    aiResponse(
        "The DHVSU Porac Campus is located in Porac, Pampanga, and is 15.06 kilometers away, west of the main "
        "campus of DHVSU in Bacolor, Pampanga.")


def public_or_private_uni():
    aiResponse("Don Honorio Ventura State University is a PUBLIC university.")


def exitApp():
    choices = ["Have a nice day!",
               "Good bye!",
               "See you soon!"]
    chosen_statement = random.choice(choices)
    aiResponse(chosen_statement)


def replay_speech():
    li = len(spoken_list) - 1
    speech = spoken_list[li]
    print("Repeating: " + speech)
    aiResponse(speech)


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
