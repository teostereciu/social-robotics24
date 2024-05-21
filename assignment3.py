'''
Assignment 2 script
Topic: 
Group6: Teodora Stereciu (s4678826) Yingsi Gao (s4706501)
Code reference: https://srl-rug.github.io/SRL_Website/examples
'''

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from utils import cards, attentions, get_drive, get_response


def decrease_attention():
    print("Losing my attention...")
    for card, _ in attentions.items():
        attentions[card] *= 0.9
    print(attentions)


def on_card(frame):
    print(frame) 
    card_id = frame['data']['body'][0][-1]
    card = cards[card_id]
    attentions[card] += 0.01

@inlineCallbacks
def main(session, details):
    global sess
    sess = session

    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sess.call("rie.dialogue.say", text="Hi, my name is Chani.")
    
    while True:
        yield sleep(1)
        decrease_attention()
        drive = get_drive()
        get_response(drive, sess)
        yield session.subscribe(on_card, "rie.vision.card.stream")
        yield session.call("rie.vision.card.stream")
        yield sleep(5)
        
        print('hey hey')
    

    # sess.leave()  # close the connection with the robot


# create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.664c6a8cf26645d6dd2bebda",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
