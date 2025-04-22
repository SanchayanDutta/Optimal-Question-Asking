import math
from collections import defaultdict

animals =  {
        "cat": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": True,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "dog": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": True,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "lion": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "elephant": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "whale": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "shark": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "eagle": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "penguin": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "crocodile": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "frog": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": True,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "snake": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "kangaroo": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "bat": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "chicken": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": True,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "cuttlefish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },

        "giraffe": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "hippopotamus": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "rhino": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "tiger": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "bear": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "panda": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "cow": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "goat": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "horse": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "monkey": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "gorilla": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "zebra": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "mouse": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "otter": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "hedgehog": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "squirrel": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "chimpanzee": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "camel": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "wolf": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "fox": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "raccoon": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "sloth": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "koala": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "buffalo": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "deer": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "moose": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },

        "sparrow": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "flamingo": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "ostrich": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "parrot": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "pelican": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "duck": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "swan": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": True,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "turkey": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "hawk": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "vulture": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },

        "lizard": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "tortoise": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": True
        },
        "turtle": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "komodo_dragon": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "chameleon": {
            "mammal": False,
            "bird": False,
            "reptile": True,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },

        "salamander": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": True,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "newt": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": True,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "toad": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": True,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },

        "salmon": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "tuna": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "clownfish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "goldfish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": True,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },

        "ant": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "bee": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "beetle": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "mosquito": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "grasshopper": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": True
        },

        "spider": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "scorpion": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },

        "octopus": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "squid": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "jellyfish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "starfish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "sea_urchin": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },

        "platypus": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "echidna": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "armadillo": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "walrus": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "seal": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "porcupine": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "donkey": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "reindeer": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        },
        "lemur": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "dolphin": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": False
        },
        "hammerhead_shark": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "manta_ray": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "eel": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "pufferfish": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": True,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "butterfly": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "moth": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "cockroach": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "dragonfly": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": True,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "crab": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "lobster": {
            "mammal": False,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": True,
            "has_fur": False,
            "domestic": False,
            "carnivore": True,
            "herbivore": False,
            "lays_eggs": True
        },
        "peacock": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "pigeon": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": True,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "emu": {
            "mammal": False,
            "bird": True,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": True,
            "can_fly": False,
            "can_swim": False,
            "has_fur": False,
            "domestic": False,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": True
        },
        "hamster": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": False,
            "lays_eggs": False
        },
        "guinea_pig": {
            "mammal": True,
            "bird": False,
            "reptile": False,
            "amphibian": False,
            "fish": False,
            "insect": False,
            "big": False,
            "can_fly": False,
            "can_swim": False,
            "has_fur": True,
            "domestic": True,
            "carnivore": False,
            "herbivore": True,
            "lays_eggs": False
        }
    }

def build_decision_tree(possible_animals, data, memo=None):
    """
    Builds a globally optimal yes/no decision tree to minimize the
    *expected* number of questions under a uniform prior over possible_animals.
    
    Returns a dict:
      {
        'type': 'attribute',
        'attribute': <attr_name>,
        'yes': <subtree_if_true>,
        'no':  <subtree_if_false>
      }
    or:
      {
        'type': 'leaf',
        'animals': <set_of_animals>  # could have 1 or more
      }
    """
    if memo is None:
        memo = {}

    # If only one animal remains, it's a leaf node with a single candidate
    if len(possible_animals) == 1:
        return {'type': 'leaf', 'animals': set(possible_animals)}

    key = frozenset(possible_animals)
    if key in memo:
        return memo[key]

    # Gather all attributes
    all_attributes = set()
    for animal in possible_animals:
        all_attributes.update(data[animal].keys())

    n = len(possible_animals)
    best_attribute = None
    best_subtree = None
    best_expected_cost = float('inf')

    if not all_attributes:
        # No attributes left to distinguish these animals:
        # Must create a leaf with all possible animals
        leaf = {'type': 'leaf', 'animals': set(possible_animals)}
        memo[key] = leaf
        return leaf

    for attribute in all_attributes:
        # Partition the animals by True vs False for this attribute
        yes_set = {a for a in possible_animals if data[a][attribute]}
        no_set = {a for a in possible_animals if not data[a][attribute]}

        # If the attribute does not split (one side empty), skip
        if not yes_set or not no_set:
            continue

        # Recursively build the subtrees
        yes_subtree = build_decision_tree(yes_set, data, memo)
        no_subtree = build_decision_tree(no_set, data, memo)

        # Expected cost: 1 + p_yes * cost(yes_subtree) + p_no * cost(no_subtree)
        p_yes = len(yes_set) / n
        p_no = 1.0 - p_yes
        cost_yes = compute_expected_cost(yes_subtree, yes_set)
        cost_no = compute_expected_cost(no_subtree, no_set)
        expected_cost = 1.0 + p_yes * cost_yes + p_no * cost_no

        if expected_cost < best_expected_cost:
            best_expected_cost = expected_cost
            best_attribute = attribute
            best_subtree = {
                'type': 'attribute',
                'attribute': attribute,
                'yes': yes_subtree,
                'no': no_subtree
            }

    # If no attribute split improved anything, leaf with all animals
    if best_subtree is None:
        leaf = {'type': 'leaf', 'animals': set(possible_animals)}
        memo[key] = leaf
        return leaf

    memo[key] = best_subtree
    return best_subtree


def compute_expected_cost(tree, possible_animals):
    """
    Given a decision tree and a uniform distribution over `possible_animals`,
    return the expected number of additional questions needed.
    """
    if tree['type'] == 'leaf':
        # No further questions needed
        return 0.0

    attribute = tree['attribute']
    yes_set = {a for a in possible_animals if animals[a][attribute]}
    no_set = {a for a in possible_animals if not animals[a][attribute]}

    n = len(possible_animals)
    if n == 0:
        return 0.0

    p_yes = len(yes_set) / n
    p_no = 1.0 - p_yes

    # 1 for this question, plus expected cost of subtrees
    cost_yes = compute_expected_cost(tree['yes'], yes_set) if yes_set else 0.0
    cost_no = compute_expected_cost(tree['no'], no_set) if no_set else 0.0
    return 1.0 + p_yes * cost_yes + p_no * cost_no


def ask_question(tree, hidden_animal):
    """
    Simulate querying the decision tree with `hidden_animal` as truth.
    Prints the asked questions, and returns the final set of possible animals.
    """
    if tree['type'] == 'leaf':
        # Might be 1 or multiple animals
        candidates = tree['animals']
        if len(candidates) == 1:
            print(f"Guessing: {next(iter(candidates))}")
        else:
            # Print all possible final candidates
            print("No more questions distinguish these. Candidates are:")
            for c in candidates:
                print("  -", c)
        return candidates

    attribute = tree['attribute']
    answer = animals[hidden_animal][attribute]
    print(f"Question: Is it '{attribute}'?  Answer: {answer}")

    if answer:
        return ask_question(tree['yes'], hidden_animal)
    else:
        return ask_question(tree['no'], hidden_animal)


if __name__ == "__main__":
    # Build the globally optimal decision tree
    all_animals = set(animals.keys())
    decision_tree = build_decision_tree(all_animals, animals)

    # Example usage: pick a hidden animal
    hidden = "guinea_pig"

    print("---- Decision Tree Query ----")
    final_candidates = ask_question(decision_tree, hidden)

    print("\nFinal candidates:", final_candidates)
    print("True animal:", hidden)
