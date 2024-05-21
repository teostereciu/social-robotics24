from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from dialogue import lines #, applause_on_keyword, is_smart_question, possible_answers


@inlineCallbacks
def positive_response():
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.right.upper.pitch": -0.2,
                                                                               "body.arms.left.lower.roll": -1.5,
                                                                               "body.arms.left.upper.pitch": -0.2,
                                                                               "body.head.pitch": 0.15}},
                                                        {"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
                                                                               "body.arms.right.upper.pitch": -0.2,
                                                                               "body.arms.left.lower.roll": -1.5,
                                                                               "body.arms.left.upper.pitch": -0.2,
                                                                               "body.head.pitch": -0.15}},
                                                        {"time": 400, "data": {"body.arms.right.lower.roll": 6e-5,
                                                                               "body.arms.right.upper.pitch": -2.5,
                                                                               "body.arms.left.lower.roll": 6e-5,
                                                                               "body.arms.left.upper.pitch": -2.5,
                                                                               "body.head.pitch": 0.1}},
                                                        {"time": 200, "data": {"body.arms.right.lower.roll": -0.6,
                                                                               "body.arms.right.upper.pitch": -2.5,
                                                                               "body.arms.left.lower.roll": -0.6,
                                                                               "body.arms.left.upper.pitch": -2.5,
                                                                               "body.head.pitch": 0.1}}
                                                        ],
                    force=True, sync=True
                    )


@inlineCallbacks
def neutral_response():

    # neutral position
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rom.optional.behavior.play", name="BlocklyShrug")


@inlineCallbacks
def negative_response():
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -1.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -1.2,
                                                                                "body.head.pitch": 0.15,
                                                                                "body.legs.right.upper.pitch": -0.4,
                                                                                "body.legs.left.upper.pitch": -0.4,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4}},
                                                        {"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -0.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -0.2,
                                                                                "body.head.pitch": 0.15,
                                                                                "body.legs.right.upper.pitch": -0.4,
                                                                                "body.legs.left.upper.pitch": -0.4,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4
                                                                                }},
                                                        {"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -1.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -1.2,
                                                                                "body.head.pitch": 0.15,
                                                                                "body.legs.right.upper.pitch": -0.4,
                                                                                "body.legs.left.upper.pitch": -0.4,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4}}
                                                        ],
                    force=True, sync=True)

