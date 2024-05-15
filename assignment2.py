'''
Assignment 2 script
Topic: 
Group6: Teodora Stereciu (s4678826) Yingsi Gao (s4706501)
Code reference: https://srl-rug.github.io/SRL_Website/examples
'''

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from dialogue import lines, applause_on_keyword, is_smart_question, possible_answers

#define keywords
#these keywords are for the break
fun_keywords = ["tell me", "fact", "tell", "fun"]
dance_keywords = ["dance", "moves", "show me", "groove", "dense", "show"]

#these keywords are for whether to continue
positive_keywords = ["yes", "ja", "yea", "sure", "of course"]
negative_keywords = ["no", "nope", "nah"]

#define on keyword function
#this function indicates the response for each keyword question
@inlineCallbacks
def on_keyword(frame):
    c = frame["data"]["body"]["certainty"]
    print("after keyword certainty", c, ": ", frame)
    if ("certainty" in frame["data"]["body"] and
            frame["data"]["body"]["certainty"] > 0.45):
        
        if frame["data"]["body"]["text"] in ['clap']:
            sess.call("rom.optional.behavior.play", name="BlocklyApplause")
        elif frame["data"]["body"]["text"] in ['bye', 'stop', 'end']:
            sess.call("rie.dialogue.say",
                      test="Alright. Bye!")
            sess.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
            sess.leave()

@inlineCallbacks
def touched(frame):
    if ("body.head.front" in frame["data"] or
        "body.head.middle" in frame["data"] or
            "body.head.rear" in frame["data"]):
        print("Why touching my head?")
        yield sess.call("rie.dialogue.say",
                        text="That was it for today. Bye for now! ")



@inlineCallbacks
def main(session, details):
    global sess
    sess = session

    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")

    yield sess.call("rie.vision.face.find")
    line = lines[0]
    yield session.call("rie.dialogue.say", text=line)  # say hello
    yield sess.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    line = lines[1]
    yield session.call("rie.dialogue.say", text=line) # introduce myself


    # introduce volcanoes
    #question = lines[1]
    #answers = {"yes": ["yes", "yeah", "sure", "yup", "yay"], "no": ["no", "nah", "nope", "nay"]}

    '''line = "Today we will dive into the fiery world of volcanoes. " + lines[4]
    yield session.call("rie.dialogue.say", text=line)

    # parts of a volcano
    line = lines[5]
    yield session.call("rie.dialogue.say", text=line)

    # magma
    line = lines[6]
    yield session.call("rie.dialogue.say", text=line)

    # vent
    line = lines[7]
    yield session.call("rie.dialogue.say", text=line)

    # crater
    line = lines[8]
    yield session.call("rie.dialogue.say", text=line)
    '''
    # erruption
    line = lines[9]
    yield session.call("rie.dialogue.say", text=line)
    line = lines[10]
    #yield session.call("rie.dialogue.say", text=line)
    
    # custom gesture
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.left.lower.roll": -1.5,
                                                                               "body.head.pitch": 0.15}}

                                                        ])
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 400, "data": {"body.head.pitch": -0.15,
                                                                               "body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.left.lower.roll": -1.5
                                                                                }
                                                        }])
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 400, "data": {"body.arms.right.lower.roll": 6e-5,
                                                                               "body.arms.left.lower.roll": 6e-5,
                                                                               "body.arms.right.upper.pitch": -2.5,
                                                                               "body.arms.left.upper.pitch": -2.5}
                                                         }], force=True)
    line = lines[10]
    yield session.call("rie.dialogue.say", text=line) #eruption
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")

    '''
    # lava
    line = lines[11]
    yield session.call("rie.dialogue.say", text=line)

    # ashes
    line = lines[12]
    yield session.call("rie.dialogue.say", text=line)'''

    # start quiz with aruco cards
    # ash question
    '''line = lines[13]
    yield session.call("rie.dialogue.say", text=line)
    # wait until we see a card
    correct = False
    cards = ['volcano', 'magma', 'vent', 'crater', 'lava', 'ash']
    while not correct:
        frames = yield session.call("rie.vision.card.read")
        print(frames[0])
        card_id = frames[0]['data']['body'][0][-1]
        print(frames[0]['data']['body'])
        if cards[card_id] == 'ash':
            correct = True
        else:
            # wrong, try again
            line = lines[14]
            yield session.call("rie.dialogue.say", text=line)
    
    # correct, move on to vent question
    line = lines[15]
    yield session.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield session.call("rie.vision.card.read")
        print(frames[0])
        card_id = frames[0]['data']['body'][0][-1]
        print(frames[0]['data']['body'])
        if cards[card_id] == 'vent':
            correct = True
        else:
            # wrong, try again
            line = lines[16]
            yield session.call("rie.dialogue.say", text=line)
   
    # correct, move on to lava question
    line = lines[17]
    yield session.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield session.call("rie.vision.card.read")
        print(frames[0])
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'vent':
            correct = True
        else:
            # wrong, try again
            line = lines[18]
            yield session.call("rie.dialogue.say", text=line)

    # correct, clap if prompted
    line = lines[19]
    yield session.call("rie.dialogue.say", text=line)
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.keyword.add",
                       keywords=['clap'])
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")
    yield sleep(7)
    yield session.call("rie.dialogue.say", text="Yes! Let's clap together.")
    yield session.call("rie.dialogue.keyword.clear")
    yield session.call("rie.dialogue.keyword.close")

    # end of the lesson
    yield sess.subscribe(touched, "rom.sensor.touch.stream")
    yield sess.call("rom.sensor.touch.stream")
    sess.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")'''



    session.leave()  #close the connection with the robot


#create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.66432728c887f6d074f07d08",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
