from twisted.internet.defer import inlineCallbacks

# define the input card labels

cards = ['volcano', 'magma', 'vent',
         'crater', 'lava', 'ash',
         'cindercone', 'lavadome', 'compositevolcano',
         'shieldvolcano', 'sunsetcrater', 'showashinjan',
         'mayon', 'maunaloa', 'arizona', 
         'japan', 'philippines', 'hawaii']



# initialize attentio
attentions = dict(zip(cards, [0]*len(cards)))

def reset_attentions():
    attentions = dict(zip(cards, [0]*len(cards)))

def increase_attention(card_id):
    """
    Increase intensity of input emotion when shown the card.
    """
    card = cards[card_id]
    attentions[card] += 0.01


def decrease_attention():
    """
    Decay the intensities of the input emotions.
    """
    for card, _ in attentions.items():
        attentions[card] *= 0.85

    print(attentions)


@inlineCallbacks
def correct_response(sess):
    """
    Implements a cheering expression for correct answers.
    """ 
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
    """
    Implements a neutral expression.
    """ 
    print('neutral resp')
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")


@inlineCallbacks
def encourage_response(sess):
    """
    Implements a encouraging expression for incorrect.
    """ 
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
    yield sess.call("rie.dialogue.say", text="You can do it! Keep trying! ")


def get_drive(correct):
    """
    Computes the drive to express emotions based on the attentions.
    """ 
    # define weights for input emotion intensity
    # for now we are only using big_emotion
    # different levels of emotions are kept for future extension
    small_emotion = 0.2
    mid_emotion = 0.4
    big_emotion = 0.6

    # initiate the scores for correct answers and incorrect answers
    score_correct = 1
    score_incorrect = 1

    for card, att in attentions.items():
        coeff = 0.6
        if correct:
            score_correct += att*coeff
        else:
            score_incorrect += att*coeff

    drive = score_correct/max(score_incorrect, 1e-16)
    return drive
    
def get_response(drive, sess):
    """
    Decide on and trigger an emotional expression based on the drive.
    """

    if drive > 0.99 and drive < 1.01:
        print('get response')
        return neutral_response(sess)
    elif drive >= 1.01:
        return correct_response(sess)
    else:
        return encourage_response(sess)
