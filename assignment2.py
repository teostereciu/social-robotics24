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

# indicates the response to keywords
@inlineCallbacks
def on_keyword(frame):
    c = frame["data"]["body"]["certainty"]
    print("after keyword certainty", c, ": ", frame)
    if ("certainty" in frame["data"]["body"] and
            frame["data"]["body"]["certainty"] > 0.45):
        
        if frame["data"]["body"]["text"] in ['clap']:
            yield sess.call("rie.dialogue.say", text="Yes! Let's clap together.") 
            sess.call("rom.optional.behavior.play", name="BlocklyApplause")
        
# indicates the response to touches
@inlineCallbacks
def touched(frame):
    # head touch prompts the session to end
    if ("body.head.front" in frame["data"] or
        "body.head.middle" in frame["data"] or
            "body.head.rear" in frame["data"]):
        print("Why touching my head?")
        yield sess.call("rie.dialogue.say",
                        text="That was it for today. Bye for now! ")
        sess.leave()


@inlineCallbacks
def main(session, details):
    global sess
    sess = session

    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")

    # look for a face, say hello and wave when found
    yield sess.call("rie.vision.face.find")
    line = lines[0]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")

    # introduce myself and lesson topic
    line = lines[1]
    yield session.call("rie.dialogue.say", text=line) 

    line = lines[2]
    yield session.call("rie.dialogue.say", text=line)

    # parts of a volcano
    line = lines[3]
    yield session.call("rie.dialogue.say", text=line)
    yield sess.call("rom.optional.behavior.play", name="BlocklyInviteRight") # built-in gesture

    # magma
    line = lines[4]
    yield session.call("rie.dialogue.say", text=line)

    # vent
    line = lines[5]
    yield session.call("rie.dialogue.say", text=line)

    # crater
    line = lines[6]
    yield session.call("rie.dialogue.say", text=line)
    
    # erruption
    line = lines[7]
    yield session.call("rie.dialogue.say", text=line)
    
    # custom gesture
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.right.upper.pitch": 0.2,
                                                                               "body.arms.left.lower.roll": -1.5,
                                                                               "body.arms.left.upper.pitch": 0.2,
                                                                               "body.head.pitch": 0.15}},
                                                        {"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.right.upper.pitch": 0.2,
                                                                               "body.arms.left.lower.roll": -1.5,
                                                                               "body.arms.left.upper.pitch": 0.2,
                                                                               "body.head.pitch": -0.15}},
                                                        {"time": 400, "data": {"body.arms.right.lower.roll": 6e-5,
                                                                               "body.arms.right.upper.pitch": -2.5,
                                                                               "body.arms.left.lower.roll": 6e-5,
                                                                               "body.arms.left.upper.pitch": -2.5,
                                                                               "body.head.pitch": 0.1}}

                                                        ],
                    force=True, sync=True
                    )
    # yield sess.call("rom.actuator.motor.write", frames=[{"time": 400, "data": {"body.head.pitch": -0.15,
    #                                                                            "body.arms.right.lower.roll": -1.5,
    #                                                                            "body.arms.left.lower.roll": -1.5
    #                                                                             }
    #                                                     }])
    # yield sess.call("rom.actuator.motor.write", frames=[{"time": 400, "data": {"body.arms.right.lower.roll": 6e-5,
    #                                                                            "body.arms.left.lower.roll": 6e-5,
    #                                                                            "body.arms.right.upper.pitch": -2.5,
    #                                                                            "body.arms.left.upper.pitch": -2.5}
    #                                                      }], force=True)
    line = lines[8]
    yield session.call("rie.dialogue.say", text=line) 
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    # end eruption
    
    # explain eruption
    line = lines[9]
    yield session.call("rie.dialogue.say", text=line) 
    
    # lava
    line = lines[10]
    yield session.call("rie.dialogue.say", text=line)

    # ashes
    line = lines[11]
    yield session.call("rie.dialogue.say", text=line)

    # start quiz with aruco cards
    # ash question
    line = lines[12]
    yield session.call("rie.dialogue.say", text=line)
    correct = False
    cards = ['volcano', 'magma', 'vent', 'crater', 'lava', 'ash']
    while not correct:
        frames = yield session.call("rie.vision.card.read")  # wait until i see a card
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'ash':
            correct = True
        else:
            # wrong, try again
            line = lines[13] # optionally replace '<>' with what the student said, so cards[card_id]
            yield session.call("rie.dialogue.say", text=line)
    
    # correct, move on to vent question
    line = lines[14]
    yield session.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield session.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'vent':
            correct = True
        else:
            # wrong, try again
            line = lines[15] # optionally replace '<>' with what the student said, so cards[card_id]
            yield session.call("rie.dialogue.say", text=line)
   
    # correct, move on to magma question
    line = lines[16]
    yield session.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield session.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'magma':
            correct = True
        else:
            # wrong, try again
            line = lines[17] # optionally replace '<>' with what the student said, so cards[card_id]
            yield session.call("rie.dialogue.say", text=line)

    # correct, clap if prompted
    line = lines[18]
    yield session.call("rie.dialogue.say", text=line)
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.keyword.add",
                       keywords=['clap'])
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")
    yield sleep(7)
    yield session.call("rie.dialogue.keyword.clear")
    yield session.call("rie.dialogue.keyword.close")

    # end of the lesson
    yield sess.subscribe(touched, "rom.sensor.touch.stream")
    yield sess.call("rom.sensor.touch.stream")
    # maybe metion that the student can end the lesson at any time and add this somewhere at the beginning? or make the bot sing at the end of the lesson until it's stopped or sth lol

    sess.leave()  # close the connection with the robot


# create wamp connection
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
