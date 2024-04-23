from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.vision.face.find")
    yield session.call("rie.dialogue.say", text="Do you want to dance?")
    yield session.call("rom.optional.behavior.play", name="BlocklyRobotDance")
    yield session.call("rie.vision.face.track")
    yield session.call("rie.dialogue.say", text="Thanks for the dance, bye!")
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
