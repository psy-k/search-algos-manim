from manim import *

cities = [            
    "s", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "r", "q", "t"
    ]

positions = {
    "s": LEFT*4.6+UP*1.47,
    "c": LEFT*3.55+UP*1.9, #dfs
    "b": LEFT*3.85+UP*1.3,
    "a": LEFT*3.9+UP*0.6, #dfs
    "d": LEFT*2.8+UP*1.4,
    "g": LEFT*3.25+UP*0.85, #dfs-2
    "f": LEFT*2.6+UP*0.45,
    "e": LEFT*3.15+UP*0.2, #dfs-2
    "h": LEFT*3.7+DOWN*0.2,
    "i": LEFT*2.4+UP*2,
    "j": LEFT*1.55+UP*1.2,
    "k": LEFT*2.4+UP*0.9,
    "l": LEFT*1.45+UP*0.6,
    "m": LEFT*1+UP*0.1,
    "n": LEFT*1.6+UP*0,
    "o": LEFT*2+DOWN*0.3,
    "p": LEFT*2.7+DOWN*0.35,
    "t": LEFT*3.2+DOWN*0.5, #dfs-3
    "r": LEFT*3.9+DOWN*0.7,
    "q": LEFT*3.2+DOWN*1.2, #dfs-3
}

labelDirections = {
    "s": LEFT,
    "c": LEFT, #dfs
    "b": DOWN,
    "a": LEFT, #dfs
    "d": DOWN,
    "g": LEFT, #dfs-2
    "f": UP,
    "e": LEFT, #dfs-2
    "h": LEFT,
    "i": LEFT,
    "j": RIGHT,
    "k": UP,
    "l": RIGHT,
    "m": DOWN,
    "n": DOWN,
    "o": LEFT,
    "p": DOWN,
    "t": DOWN, #dfs-3
    "r": LEFT,
    "q": LEFT, #dfs-3
}

adjLists = {
    "s": ["a", "b", "c"],
    "c": ["b", "g", "s"], #dfs-1
    "b": ["c", "d", "g", "s"],
    "a": [ "h", "e", "f", "s"], #dfs-1
    "d": ["b", "i", "j", "k"],
    "g": ["a", "b", "k"], #dfs-2
    "f": ["a", "l", "m", "n", "o"],
    "e": [ "t", "a", "k", "p"], #dfs-2
    "h": ["a", "r", "q"],
    "i": ["d"],
    "j": ["d", "k"],
    "k": ["e", "e", "l", "d", "j"],
    "l": ["k", "f"],
    "m": ["f", "n"],
    "n": ["m", "f"],
    "o": ["f"],
    "p": ["e"], 
    "t": [ "e"], #dfs-3
    "r": ["h"],
    "q": ["h"] #dfs-3
}

