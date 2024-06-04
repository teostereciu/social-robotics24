'''
Final Assignment script
Topic: Interactive Lesson about Volcanoes with Alpha Mini
Group6: Teodora Stereciu (s4678826) & Yingsi Gao (s4706501)
'''

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from parts_lesson import test_volcano_parts
from types_lesson import teach_volcano_types, test_volcano_types
from utils import cards, attentions, get_drive, get_response


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
    yield session.call("rie.dialogue.config.language", lang="en")
    ########### introduction ###########
    yield sess.call("rom.optional.behavior.play", name="BlocklyStand")
    #yield sess.call("rie.dialogue.say", text="Hi, my name is Chani. Show me how you are feeling today.")
   
    ########### lesson about volcano parts ###########
    # teach
    # question
    #test_volcano_parts(sess)
    # break

    ########### lesson about types of volcanoes ###########
    # teach
    print('main')
    teach_volcano_types(sess)
    #test_volcano_types(sess)
    # question
    # break
    
    ########### end of the lesson ###########
    yield sess.leave()


# create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.665ec56e29fca0a53366cd30",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
