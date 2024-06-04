from utils import cards


lines = [
    "First, let me show you the parts of a volcano.",
    "Think of the volcano as a big mountain. Underground, there is magma. Magma is hot molten rock.",
    "In the middle of the mountain, there is a main vent. The magma flows through the vent.",
    "On top of the mountain, there is a crater. The vent connects to the crater.",
    "But, volcano is not your average mountain. It will erupt sometimes.",
    "Underground, magma slowly accumulate. When the pressure builds up, it has nowhere to go but up the main vent.",
    "When the magma reaches the crater...",
    "And poof.",
    "Lava runs out and ashes rise up into the sky.",

    "Do you remember which one is the ash?", #9
    "No. Remember? The ash is a gray cloud above the volcano!",
    "Yes! That's correct. Can you now show me the vent of a volcano?",
    "No. Try again. Remember the vent in in the middle of the volcano.",
    "That's right! What runs through the vent? Can you show me?",
    "No. Remember that lava is molten rock that reached the surface. Underground molten rock is called magma!",
    "Good job! That was a tricky one."
]

eruption_gesture_pressure = [
    {"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
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
]

eruption_gesture_explode = [
{"time": 200, "data": {"body.arms.right.lower.roll": -1.5,
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
]


def teach_volcano_parts(sess):
    """
    Gives a short lesson about the major volcano parts.
    """
    # parts of a volcano
    line = lines[0]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.optional.behavior.play", name="BlocklyInviteRight")  # built-in gesture

    # magma
    line = lines[1]
    yield sess.call("rie.dialogue.say", text=line)

    # vent
    line = lines[2]
    yield sess.call("rie.dialogue.say", text=line)

    # crater
    line = lines[3]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")

    # erruption
    line = lines[4]
    yield sess.call("rie.dialogue.say", text=line)
    line = lines[5]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.actuator.motor.write", frames=eruption_gesture_pressure, force=True, sync=True)
    line = lines[6]
    yield sess.call("rie.dialogue.say", text=line)
    line = lines[7]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.actuator.motor.write", frames=eruption_gesture_explode, force=True, sync=True)
    line = lines[8]
    yield sess.call("rie.dialogue.say", text=line)
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")


def test_volcano_parts(sess):
    """
    Gives a short quiz on major volcano parts.
    """
    line = lines[9]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield sess.call("rie.vision.card.read")  # wait until i see a card
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'ash':
            correct = True
        else:
            # wrong, try again
            line = lines[10]  # optionally replace '<>' with what the student said, so cards[card_id]
            yield sess.call("rie.dialogue.say", text=line)

    # correct, move on to vent question
    line = lines[11]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield sess.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'vent':
            correct = True
        else:
            # wrong, try again
            line = lines[12]  # optionally replace '<>' with what the student said, so cards[card_id]
            yield sess.call("rie.dialogue.say", text=line)

    # correct, move on to magma question
    line = lines[13]
    yield sess.call("rie.dialogue.say", text=line)
    correct = False
    while not correct:
        frames = yield sess.call("rie.vision.card.read")
        card_id = frames[0]['data']['body'][0][-1]
        if cards[card_id] == 'magma':
            correct = True
        else:
            # wrong, try again
            line = lines[14]  # optionally replace '<>' with what the student said, so cards[card_id]
            yield sess.call("rie.dialogue.say", text=line)

    # correct
    line = lines[15]
    yield sess.call("rie.dialogue.say", text=line)


def take_a_break_from_parts(sess):
    """
    Lets the student take a break. 
    At their request, Alpha Mini can do a dance or offer a fun fact about volcano parts.
    """
    # dance
    yield sess.call("rom.optional.behavior.play", name="BlocklyRobotDance")
