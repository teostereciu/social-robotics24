import random

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

lecture_lines = [
    "Now that we've seen different parts of a volcano. Let me show you the different types of volcanoes.",
    "Cinder cone volcanoes are the most common type. They are also the smallest.",
    "For example, Sunset Crater is a cinder cone volcano. It has a single crater fed by only one vent.",
    "Another type of volcano is a Lava Dome. It is also on the smaller side with limited volume.",
    "For example, Showa Shinjan is a lava dome volcano. It has steep sides and rough surface."
    "There are also composite volcanoes which are bigger. Their eruptions are huge!",
    "For example, Mayon is a compositive volcano. It has very steep sides and the lava does not flow far.",
    "Finally, we also talk about Shield Volcanoes. They are much wider than they are tall.",
    "For example, Mauna Loa is a shield volcano. The intermediate period between eruptions are usually millions of years. When it erupts, liquid lava flows out.",
    "Are you ready to see these volcanoes on a map?",
    "Cool! Here's the map of the world. Sunset Crater is in the USA. Showa Shinjan is in Japan. Mayon is in the Phillippines. Mauna Loa is in Hawaii.",
    "Okay. Let's have a break first, and then see the map together.",
]

quiz_lines = [
    "Do you remember which type of volcano is the most common?",
    "No. That's not it. Remember the most common type of volcano is the smallest and has one vent and crater.",
    "Yes! That's correct. Can you give me an example of a cinder cone volcano from the lecture?",
    "No. Try again, you've got this!",
    "That's right! Do you know where is this volcano?",
    "No. it's in North America! Can you remember the country?",
    "Good job! That was a tricky one. Let's clap together for you!"
]

fun_facts = [
    'fun',
    'fun',
    'fun'
]


def teach_volcano_types(sess):
    """
    Gives a short lesson about the major volcano types.
    """
    # start
    line = lecture_lines[0]
    yield sess.call("rie.dialogue.say", text=line)

    # cinder cone
    line = lecture_lines[1] + lecture_lines[2]
    yield sess.call("rie.dialogue.say", text=line)

    # lava dome
    line = lecture_lines[3] + lecture_lines[4]
    yield sess.call("rie.dialogue.say", text=line)

    # composite
    line = lecture_lines[5] + lecture_lines[6]
    yield sess.call("rie.dialogue.say", text=line)
    
    # shield
    line = lecture_lines[7] + lecture_lines[8]
    yield sess.call("rie.dialogue.say", text=line)
    
    question = lecture_lines[9]
    answer = yield sess.call("rie.dialogue.ask",
                             question=question,
                             answers={'yes':['yes', 'yeah', 'yup', 'yay'],
                                      'no' :['no', 'nah', 'nope', 'nay']})
    if answer == "yes":
        line = lecture_lines[10]
        yield sess.call("rie.dialogue.say",
        text=line)
    elif answer == "no":
        line = lecture_lines[11]
        yield sess.call("rie.dialogue.say",
        text=line)
        take_a_break_from_types(sess)
    else:
        yield sess.call("rie.dialogue.say",
        text="Sorry, but I didn't hear you properly. Yes or no?")
    
    yield sess.call("rie.dialogue.stop")
    

def test_volcano_types(sess):
    """
    Gives a short quiz on major volcano types.
    """
    # easy question
    line = quiz_lines[0]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    cards = []
    while not correct:
        frames = yield sess.call("rie.vision.card.read")  # wait until i see a card
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'cinder cone':
            correct = True
        else:
            # wrong, try again
            line = quiz_lines[1] 
            yield sess.call("rie.dialogue.say", text=line)
    
    # correct, move on to medium question
    line = quiz_lines[2]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield sess.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'vent':
            correct = True
        else:
            # wrong, try again
            line = quiz_lines[3] 
            yield sess.call("rie.dialogue.say", text=line)
   
    # correct, move on to difficult question
    line = quiz_lines[4]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield sess.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'magma':
            correct = True
        else:
            # wrong, try again
            line = quiz_lines[5] 
            yield sess.call("rie.dialogue.say", text=line)

    # correct, congratulate and clap in main
    line = quiz_lines[6]
    yield sess.call("rie.dialogue.say", text=line)


def take_a_break_from_types(sess):
    """
    Lets the student take a break. 
    Alpha Mini will offer a fun fact about volcano types.
    """
    yield sleep(5)
    selected_fact = random.choice(fun_facts)
    yield sess.call("rie.dialogue.say", text=['While you are resting, let me tell you a quick fun fact! '] + selected_fact)
    yield sleep(5)
