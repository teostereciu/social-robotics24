from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyArmsForward")
    print("stand ok")
    yield session.call("rom.actuator.motor.write",
		frames=[{"time": 500, "data": {"body.arms.right.upper.pitch": -1.2}},
			],
		force=True
	)

    yield sleep(2)
    session.leave() # Close the connection with the robot
    #yield session.subscribe(touched, "rom.sensor.touch.stream")
    #yield session.call("rom.sensor.touch.stream")

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
