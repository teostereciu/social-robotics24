from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    question1 = "Do you want to test your Geography knowledge with a quiz?"
    answers = {"yes": ["yes", "yeah", "sure", "yup", "yay"], "no": ["no", "nah", "nope", "nay"]} 
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    #yield session.call("rie.vision.face.find")
    yield session.call("rie.dialogue.say", text="Hello. My name is Chani.")
    answer = yield session.call("rie.dialogue.ask",
                                question=question1,
                                answers=answers) 
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
    
    
    question2 = "What's the capital city of the UK?"
    answers2 = {"london": ["London", "london", "lon", "don", "lomdom", 'lomndomn', 'London?', 'London!']}

    #cnt = 0
    #max_cnt = 2

    answer = yield session.call("rie.dialogue.ask",
                                question=question2,
                                answers=answers2,
                                max_attempts=10)

    if answer == "london":
        yield session.call("rie.dialogue.say",
        text="Good job!")
    else:
        #cnt +=1
        #if cnt <= max_cnt:
        #    yield session.call("rie.dialogue.say",
        #                       text="Sorry, but I didn't hear you properly. Try again.")
        #else:
        yield session.call("rie.dialogue.say",
                               text="Sorry, ran out of attempts.")
            #session.leave()
            
    
    

    session.leave() 

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
