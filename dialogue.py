lines = ["Hello!",
         "My name is Chani! Today, I'll teach you about volcanoes.",
         "No worries! Let me show you a volcano. I'll tell you more about the fiery world of volcanoes.",
         "Awesome! Today we will dive into the fiery world of volcanoes.",
         "They might look scary, but they are actually pretty fascinating.",

         "First, let me show you the parts of a volcano.",
         "Think of the volcano as a big mountain. Underground, there is magma. Magma is hot molten rock.",
         "In the middle of the mountain, there is a main vent. The magma flows through the vent.",
         "On top of the mountain, there is a crater. The vent connects to the crater.",
         "But, a volcano is not your average mountain. It will sometimes. ",
         "Erupt! ",

         """Underground, magma slowly accumulate. When the pressure builds up, it has nowhere to go but up the main vent. 
         When the magma reaches the crater... Poof!""",
         "Lava runs out...",
         "and ashes rise up into the sky.",
         "Do you remember which one is the ash?",
         "No. That's the <>. The ash is a gray cloud above the volcano!",

         "Yes! That's correct. Can you now show me the vent of a volcano?",
         "No. This is the <>. The vent in in the middle of the volcano.",
         "That's right! What runs through the vent? Can you show me?",
         "No. Remember that lava is molten rock that reached the surface. Underground molten rock is called magma!",
         "Good job! That was a tricky one. Let's clap together for you! Say clap Chani!"
         ]

volcano_gesture_on_line = 10
applause_on_keyword = ["clap"]
is_smart_question = [False, True, False, False, False, 
                     False, False, False, False, False, 
                     False, False, True, False, True, 
                     False, True, False, False]

show_card = [None, None, 'volcano', None, 'volcano', 
             None, 'magma', 'vent', 'crater', None, 
             None, 'lava', 'ash', None, 'ash', 
             None, 'vent', None, 'lava', None]

# some behavior for not showing a card when prompted

possible_answers = [{}, 
                    {"yes":["yes", "yeah"], "no": ["no", "nah"]},
                    {},
                    {},
                    {},

                    {},
                    {},
                    {},
                    {},
                    {},

                    {},
                    {},
                    {},
                    {"right_card":['ash'], "wrong_card":['volcano', 'magma', 'vent', 'crater', 'lava']},
                    {},
                    
                    {"right_card":['vent'], "wrong_card":['volcano', 'magma', 'ash', 'crater', 'lava']},
                    {},
                    {"right_card":['lava'], "wrong_card":['volcano', 'magma', 'ash', 'crater', 'vent']},
                    {},
                    {},
                    ]