'''
Assignment 3 script
Topic: Emotion regulation and expression
Group6: Teodora Stereciu (s4678826) & Yingsi Gao (s4706501)
'''

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from utils import cards, attentions, get_drive, get_response


def decrease_attention():
    """
    Decay the intensities of the input emotions.
    """
    for card, _ in attentions.items():
        attentions[card] *= 0.85 


def on_card(frame):
    """
    Increase intensity of input emotion when shown the card.
    """
    card_id = frame['data']['body'][0][-1]
    card = cards[card_id]
    attentions[card] += 0.01


@inlineCallbacks
def main(session, details):
    global sess
    sess = session

    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rie.dialogue.say", text="Hi, my name is Chani. Show me how you are feeling today.")
    
    while True:
        yield sleep(1)
        decrease_attention()
        drive = get_drive()
        get_response(drive, sess)
        yield sess.subscribe(on_card, "rie.vision.card.stream")
        yield sess.call("rie.vision.card.stream")
        yield sleep(5)


# create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.6655a01bf26645d6dd2c1e70",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
