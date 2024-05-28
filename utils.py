from twisted.internet.defer import inlineCallbacks


cards = ['boredom', 'disgust', 'loathing',
         'admiration', 'trust', 'acceptance',
         'interest', 'anticipation', 'vigilance',
         'distraction', 'surprise', 'amazement']

pos = ['admiration', 'trust', 'acceptance', 'interest', 'anticipation', 'vigilance']

attentions = dict(zip(cards, [0]*len(cards)))

@inlineCallbacks
def positive_response(sess): 
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
                                                                               "body.head.pitch": -0.17}},
                                                        {"time": 200, "data": {"body.arms.right.lower.roll": -0.6,
                                                                               "body.arms.right.upper.pitch": -2.5,
                                                                               "body.arms.left.lower.roll": -0.6,
                                                                               "body.arms.left.upper.pitch": -2.5,
                                                                               "body.head.pitch": -0.17}}
                                                        ],
                    force=True, sync=True
                    )
    yield sess.call("rie.dialogue.say", text="Yay!")


@inlineCallbacks
def neutral_response(sess):

    # neutral position
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rom.optional.behavior.play", name="BlocklyShrug")


@inlineCallbacks
def negative_response(sess):
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rom.actuator.motor.write", frames=[{"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -1.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -1.2,
                                                                                "body.head.pitch": 0.15,
                                                                                "body.legs.right.upper.pitch": -0.45,
                                                                                "body.legs.left.upper.pitch": -0.45,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4}},
                                                        {"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -0.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -0.2,
                                                                                "body.head.pitch": 0.17,
                                                                                "body.legs.right.upper.pitch": -0.45,
                                                                                "body.legs.left.upper.pitch": -0.45,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4
                                                                                }},
                                                        {"time": 1000, "data": {"body.arms.right.lower.roll": -1.5,
                                                                                "body.arms.right.upper.pitch": -1.2,
                                                                                "body.arms.left.lower.roll": -1.5,
                                                                                "body.arms.left.upper.pitch": -1.2,
                                                                                "body.head.pitch": 0.17,
                                                                                "body.legs.right.upper.pitch": -0.45,
                                                                                "body.legs.left.upper.pitch": -0.45,
                                                                                "body.legs.right.lower.pitch": 0.4,
                                                                                "body.legs.left.lower.pitch": 0.4}}
                                                        ],
                    force=True, sync=True)
    yield sess.call("rie.dialogue.say", text="Oh nooo...")

def get_drive():
    small_emotion = 0.2
    mid_emotion = 0.4
    big_emotion = 0.6

    score_pos = 1
    score_neg = 1

    for card, att in attentions.items():
        if cards.index(card) % 4 == 0:
            coeff = small_emotion
        elif cards.index(card) % 4 == 1:
            coeff = mid_emotion
        else:
            coeff = big_emotion
        if card in pos:
            score_pos += att*coeff
        else:
            score_neg += att*coeff

    drive = score_pos/max(score_neg, 1e-16)
    return drive
    
def get_response(drive, sess):
    print('drive', drive)
    if drive > 0.9 and drive < 1.1:
        return neutral_response(sess)
    elif drive >= 1.05:
        return positive_response(sess)
    else:
        return negative_response(sess)
