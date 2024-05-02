from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

#define keywords
fun_keywords = ["tell me", "fun fact", "random fact", "fact", "facts", "some fact", "tell"]
dance_keywords = ["dance", "moves", "show me", "groove", "dense", "show"]


#define on keyword function
@inlineCallbacks
def on_keyword(frame):
    c = frame["data"]["body"]["certainty"]
    print("after keyword certainty", c, ": ", frame)
    if ("certainty" in frame["data"]["body"] and
            frame["data"]["body"]["certainty"] > 0.45):
        if frame["data"]["body"]["text"] in fun_keywords:
            sess.call("rie.dialogue.say",
                      text="Do you know that the capital city of the Netherlands is Amsterdam. ")
        elif frame["data"]["body"]["text"] in dance_keywords:
            sess.call("rom.optional.behavior.play", name="BlocklyRobotDance")


@inlineCallbacks
def main(session, details):
    global sess
    sess = session
    #first question
    question1 = "Do you want to test your Geography knowledge with a quiz?"
    answers1 = {"yes": ["yes", "yeah", "sure", "yup", "yay"], "no": ["no", "nah", "nope", "nay"]}

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.dialogue.say", text="Hello. My name is Chani.")
    answer = yield session.call("rie.dialogue.ask",
                                question=question1,
                                answers=answers1)
    if answer == "yes":
        yield session.call("rie.dialogue.say",
        text="Cool! Let's start!")
    elif answer == "no":
        yield session.call("rie.dialogue.say",
        text="Ok, bye!")
        session.leave() 
    else:
        yield session.call("rie.dialogue.say",
        text="Sorry, but I didn't hear you properly. Yes or no?")
    
    #second question
    question2 = "What's the capital city of the UK?"
    answers2 = {"london": ["London", "london", "lon", "don", "lomdom", 'lomndomn', 'London?', 'London!']}

    answer = yield session.call("rie.dialogue.ask",
                                question=question2,
                                answers=answers2,
                                max_attempts=5)

    if answer == "london":
        yield session.call("rie.dialogue.say",
        text="Good job!")

        #ask a harder question
        question3 = "What's the capital city of Nigeria?"
        answers3 = {"abuja": ["abuja", "Abuja"]}
        answer = yield session.call("rie.dialogue.ask",
                                    question=question3,
                                    answers=answers3,
                                    max_attempts=5)
        if answer == "abuja":
            yield session.call("rie.dialogue.say",
                               text="Excellent! You're doing great!")
        else:
            yield session.call("rie.dialogue.say",
                               text="Sorry, incorrect answer. The capital city of Nigeria is Abuja. ")

    else:
        yield session.call("rie.dialogue.say",
                           text="Sorry. The capital city of the UK is London. ")



    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.say_animated",
                       text="Time for a break, you can ask me for a dance or a fun fact. ")

    yield session.call("rie.dialogue.keyword.add",
                       keywords=fun_keywords + dance_keywords)
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")

    printy = yield session.call("rie.dialogue.stt.read", time=6000)
    print("printy", printy, "\n")
    # Please wait 20 seconds before we close the keyword stream
    yield sleep(20)
    yield session.call("rie.dialogue.say", text="Okay.")
    yield session.call("rie.dialogue.keyword.clear")
    yield session.call("rie.dialogue.keyword.close")

    session.leave()  # Close the connection with the robot

        # Create wamp connection

wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.6627761294f6248b6e0d4647",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
