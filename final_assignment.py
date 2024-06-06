'''
Final Assignment script
Topic: Interactive Lesson about Volcanoes with Alpha Mini
Group6: Teodora Stereciu (s4678826) & Yingsi Gao (s4706501)
'''

from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from parts_lesson import teach_volcano_parts, test_volcano_parts
from types_lesson import teach_volcano_types, test_volcano_types
from utils import cards, attentions, get_drive, get_response


# indicates the response to keywords
@inlineCallbacks
def on_keyword(frame):
    c = frame["data"]["body"]["certainty"]
    print("after keyword certainty", c, ": ", frame)
    if ("certainty" in frame["data"]["body"] and
            frame["data"]["body"]["certainty"] > 0.45):
        
        if frame["data"]["body"]["text"] in ['clap']:
            yield sess.call("rie.dialogue.say", text="Yes! Let's clap together.") 
            sess.call("rom.optional.behavior.play", name="BlocklyApplause")
    

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
    yield sess.call("rie.vision.face.find")
    yield sess.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
    line = "Hi my name is Chani. Today I'll teach you about volcanoes."
    yield sess.call("rie.dialogue.say", text=line)
    
    '''question = "Are you ready?"
    answer = yield sess.call("rie.dialogue.ask",
                             question=question,
                             answers={'yes':['yes', 'yeah', 'yup', 'yay'],
                                      'no' :['no', 'nah', 'nope', 'nay']})
    '''
    answer="no"
    if answer == "yes":
        line = "Awesome! Today we wll dive into the fiery world of volcanoes."
        yield sess.call("rie.dialogue.say",
        text=line)
        line= "Here is a volcano. They might look scary but they are actually pretty fascinating."
        yield sess.call("rie.dialogue.say",
        text=line)
    elif answer == "no":
        line = "No worries! Let me start with a fun fact"
        yield sess.call("rie.dialogue.say",
        text=line)
        line = "Do you know that there are more than 15000 volcanoes around the world. Here's a map. Each red dot on the map represents a volcano site."
        yield sess.call("rie.dialogue.say",
        text=line)
    else:
        yield sess.call("rie.dialogue.say",
        text="Sorry, but I didn't hear you properly. Yes or no?")
    
    yield sess.call("rie.dialogue.stop")

    ########### lesson about volcano parts ###########
    yield teach_volcano_parts(sess)
    yield test_volcano_parts(sess)
    
    ########### lesson about types of volcanoes ###########
    yield teach_volcano_types(sess)
    yield test_volcano_types(sess)
    
    ########### end of the lesson ###########
    
    line = "This is the end of today's lesson. Let's give you applause for your work. Say clap Chani!"
    yield session.call("rie.dialogue.say", text=line)
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.keyword.add",
                       keywords=['clap'])
    yield session.subscribe(on_keyword,
                            "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")
    yield sleep(7)
    yield session.call("rie.dialogue.keyword.clear")
    yield session.call("rie.dialogue.keyword.close")
    
    yield sess.leave()


# create wamp connection
wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"]
    }],
    realm="rie.666187af29fca0a53366e071",
)


wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
