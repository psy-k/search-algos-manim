from manim import *

cities = [            
    "s", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "t"
    ]

positions = {
    "s": LEFT*4.6+UP*1.47,
    "a": LEFT*3.55+UP*1.9,
    "b": LEFT*3.85+UP*1.3,
    "c": LEFT*3.9+UP*0.6,
    "d": LEFT*2.8+UP*1.4,
    "e": LEFT*3.25+UP*0.85,
    "f": LEFT*2.6+UP*0.45,
    "g": LEFT*3.15+UP*0.2,
    "h": LEFT*3.7+DOWN*0.2,
    "i": LEFT*2.4+UP*2,
    "j": LEFT*1.55+UP*1.2,
    "k": LEFT*2.4+UP*0.9,
    "l": LEFT*1.45+UP*0.6,
    "m": LEFT*1+UP*0.1,
    "n": LEFT*1.6+UP*0,
    "o": LEFT*2+DOWN*0.3,
    "p": LEFT*2.7+DOWN*0.35,
    "q": LEFT*3.2+DOWN*0.5,
    "r": LEFT*3.9+DOWN*0.7,
    "t": LEFT*3.2+DOWN*1.2,
}

labelDirections = {
    "s": LEFT,
    "a": LEFT,
    "b": DOWN,
    "c": LEFT,
    "d": DOWN,
    "e": LEFT,
    "f": UP,
    "g": LEFT,
    "h": LEFT,
    "i": LEFT,
    "j": RIGHT,
    "k": UP,
    "l": RIGHT,
    "m": DOWN,
    "n": DOWN,
    "o": LEFT,
    "p": DOWN,
    "q": DOWN,
    "r": LEFT,
    "t": LEFT,
}

adjLists = {
    "s": ["a", "b", "c"],
    "a": ["b", "e", "s"],
    "b": ["a", "d", "e", "s"],
    "c": ["f", "g", "h", "s"],
    "d": ["b", "i", "j"],
    "e": ["a", "b", "k"],
    "f": ["c", "l", "m", "n", "o", "q"],
    "g": ["c", "k", "p", "q"],
    "h": ["c", "r", "t"],
    "i": ["d"],
    "j": ["d"],
    "k": ["e", "g", "l"],
    "l": ["k", "f"],
    "m": ["f", "n"],
    "n": ["m", "f"],
    "o": ["f"],
    "p": ["g", "r"],
    "q": ["f", "g"],
    "r": ["h", "p", "t"],
    "t": ["h", "r"]
}

