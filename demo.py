from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    def on_keyword(frame):
        print("after keyword", frame)
        if ("certainty" in frame["data"]["body"] and
                frame["data"]["body"]["certainty"] > 0.45):
            if frame["data"]["body"]["text"] in fun_keywords:
                session.call("rie.dialogue.say", text="Do you know that the capital city of the Netherlands is Amsterdam. ")
            elif frame["data"]["body"]["text"] in dance_keywords:
                session.call("rom.optional.behavior.play", name="BlocklyRobotDance")

    yield session.call("rie.dialogue.say",
                       text="Time for a break, you can ask me for a dance or a fun fact. ")
    fun_keywords = ["tell me", "fun fact", "random fact", "fact", "facts", "some fact", "tell"]
    dance_keywords = ["dance", "moves", "show me", "groove", "dense", "show", "then", "1"]
    yield session.call("rie.dialogue.keyword.add",
                       keywords=fun_keywords+dance_keywords)
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")

    printy = yield session.call("rie.dialogue.stt.read", time=6000)
    print("printy", printy, "\n")
    # Please wait 20 seconds before we close the keyword stream
    yield sleep(50)
    yield session.call("rie.dialogue.keyword.close")
    yield session.call("rie.dialogue.keyword.clear")
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

