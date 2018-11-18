from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from playsound import playsound

AVAILABLE_NOTES = (
    'A',
    'A#',
    'B',
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
    'R',  # Rest note
)


class Note(ABC):
    @abstractmethod
    def play(self):
        pass


class AudioNote(Note):
    def __init__(self, name):
        self.name = name
        self.file = 'notes/{}.wav'.format(name)

    def play(self):
        playsound(self.file)

    def __str__(self):
        return self.name


class ChordNote(Note):
    def __init__(self, notes):
        self.notes = notes

    def play(self):
        for note in self.notes:
            Thread(target=note.play).start()

    def __str__(self):
        return str(self.notes)


class RestNote(Note):
    def __init__(self, time=0.2):
        self.time = time

    def play(self):
        sleep(self.time)

    def __str__(self):
        return "R"


class Melody(list):
    def play(self):
        for note in self:
            note.play()

    def __str__(self):
        ret = ""
        for item in self:
            ret += str(item)
        return ret
