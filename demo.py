from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyMacarena")
	# Nod
    yield session.call("rom.actuator.motor.write",
		frames=[{"time": 400, "data": {"body.arms.right.upper.pitch": -2.60}},
			{"time": 1200, "data": {"body.arms.right.lower.roll": -1.75}},
		    ],
		force=True
	)
    yield sleep(2)
    def touched(frame):
        cnt = 0
        max_cnt = 0
        
        if ("body.head.front" in frame["data"] and frame["data"]["body.head.front"]):
            session.call("rie.dialogue.say", text="It's so sunny today!")
            cnt += 1
            if cnt >= max_cnt:
                session.leave() # Close the connection with the robot
            
        elif ("body.head.middle" in frame["data"] and frame["data"]["body.head.middle"]):
            session.call("rie.dialogue.say", text="Aww it's raining a lot!")
            cnt += 1
            if cnt >= max_cnt:
                session.leave() # Close the connection with the robot
            
        elif ("body.head.rear" in frame["data"] and frame["data"]["body.head.rear"]):
            session.call("rie.dialogue.say", text="What?! Snow in April?")
            cnt += 1
            if cnt >= max_cnt:
                session.leave() # Close the connection with the robot
            
    yield sleep(2)
    yield session.subscribe(touched, "rom.sensor.touch.stream")
    yield session.call("rom.sensor.touch.stream")

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
