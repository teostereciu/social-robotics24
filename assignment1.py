from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

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
        if frame["data"]["body"]["text"] in fun_keywords:
            sess.call("rie.dialogue.say",
                      text="Do you know that the UK is home to the world's oldest underground railway system. ")
        elif frame["data"]["body"]["text"] in dance_keywords:
            sess.call("rom.optional.behavior.play", name="BlocklyRobotDance")
        elif frame["data"]["body"]["text"] in positive_keywords:
            sess.call("rie.dialogue.say",
                      text="Okay. Next question.")
        elif frame["data"]["body"]["text"] in negative_keywords:
            sess.call("rie.dialogue.say",
                      test="Alright. Bye!")
            sess.leave()


@inlineCallbacks
def main(session, details):
    global sess
    sess = session
    #first question to start the lesson
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
    yield session.call("rie.dialogue.stop")

    #second question
    #geography question
    question2 = "What's the capital city of the UK?"
    answers2 = {"london": ["London", "london", "lon", "don", "lomdom", 'lomndomn', 'London?', 'London!'], "no": ["I don't know.", "no idea", "no"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question2,
                                answers=answers2,
                                max_attempts=5)

    if answer == "london":
        yield session.call("rie.dialogue.say",
        text="Good job!")

        #the kid get the basic question right
        #ask a harder question
        question3 = "Next question. What's the capital city of Nigeria?"
        answers3 = {"abuja": ["abuja", "Abuja"], "no": ["I don't know.", "no idea", "no"]}
        answer = yield session.call("rie.dialogue.ask",
                                    question=question3,
                                    answers=answers3,
                                    max_attempts=5)
        if answer == "abuja":
            yield session.call("rie.dialogue.say",
                               text="Excellent! You're doing great!")
        elif answer == "no":
            yield session.call("rie.dialogue.say",
                               text="The capital city of Nigeria is Abuja.")
        else:
            yield session.call("rie.dialogue.say",
                               text="Sorry, incorrect answer. The capital city of Nigeria is Abuja. ")
    elif answer == "no":
        yield session.call("rie.dialogue.say",
                           text="The capital city of the UK is London. ")

        #when the basic question is answered wrong
        #the kid may choose to try another question or stop
        yield session.call("rie.dialogue.config.language", lang="en")
        yield session.call("rie.dialogue.keyword.language", lang="en")
        yield session.call("rie.dialogue.say",
                           text="Do you want to try another one?")

        yield session.call("rie.dialogue.keyword.add",
                           keywords=positive_keywords+negative_keywords)
        yield session.subscribe(on_keyword,
                                "rie.dialogue.keyword.stream")
        yield session.call("rie.dialogue.keyword.stream")
        # Please wait 7 seconds before we close the keyword stream
        yield sleep(7)
        yield session.call("rie.dialogue.say", text="Okay.")
        yield session.call("rie.dialogue.keyword.clear")
        yield session.call("rie.dialogue.keyword.close")

    else:
        yield session.call("rie.dialogue.say",
                           text="Sorry. The capital city of the UK is London. ")
        yield session.call("rie.dialogue.say",
                           text="I'll ask an easier question. ")

    #to restore the kid's confidence
    #easy question follows
    question4 = "Which country has the capital city Paris? "
    answers4 = {"france": ["France", "france", "french"]}
    answer = yield session.call("rie.dialogue.ask",
                                question=question4,
                                answers=answers4,
                                max_attempts=3)
    if answer == "france":
        yield session.call("rie.dialogue.say",
                           text="Good job!")
    else:
        yield session.call("rie.dialogue.say",
                           text="Paris is in France. ")


    #it has been a while
    #a break implemented
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.say",
                       text="Time for a break, you can ask me for a dance or a fun fact. ")

    yield session.call("rie.dialogue.keyword.add",
                       keywords=fun_keywords + dance_keywords)
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")
    # Please wait 7 seconds before we close the keyword stream
    yield sleep(7)
    yield session.call("rie.dialogue.say", text="Okay.")
    yield session.call("rie.dialogue.keyword.clear")
    yield session.call("rie.dialogue.keyword.close")

    #back to questions
    yield session.call("rie.dialogue.say",
                       text="Back to questions. ")
    question5 = "Which country is London the capital city of?"
    answers5 = {"uk": ["UK", "United Kingdom", "Britain", "England", "Great Britain", "Briton"]}
    yield session.call("rie.dialogue.ask",
                       question=question5,
                       answers=answers5,
                       max_attempts=5)

    if answer == "uk":
        yield session.call("rie.dialogue.say",
                           text="Correct! London is the capital city of the United Kingdom.")
    else:
        yield session.call("rie.dialogue.say", text="Sorry, incorrect answer.London is the capital city of the United Kingdom.")

    #the end of the lesson
    yield session.call("rie.dialogue.say",
                       text="That was the last question of the day. Bye for now! ")

    session.leave()  #close the connection with the robot


#create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.66334b92c887f6d074f02f01",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
