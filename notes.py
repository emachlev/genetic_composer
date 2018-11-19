from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from playsound import playsound


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
        threads = []
        for note in self.notes:
            thread = Thread(target=note.play)
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

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


if __name__ == '__main__':
    # Play Shape of You
    m1 = Melody([
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5D#'),
        RestNote(),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('4B'),
    ])

    m2 = Melody([
        AudioNote('4C#'),
        RestNote(),
        AudioNote('4C#'),
        RestNote(),
        AudioNote('4C#'),
        AudioNote('3F#'),
        RestNote(),
        AudioNote('3F#'),
        RestNote(),
        AudioNote('3F#'),
        AudioNote('3A'),
        RestNote(),
        AudioNote('3A'),
        RestNote(),
        AudioNote('3A'),
        AudioNote('3B'),
        RestNote(),
        AudioNote('3B'),
        RestNote(),
        AudioNote('3B'),
    ])

    while True:
        t1 = Thread(target=m1.play)
        t2 = Thread(target=m2.play)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
