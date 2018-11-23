from abc import ABC, abstractmethod
from threading import Thread
from time import sleep
from difflib import SequenceMatcher
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

    def distance(self, note):
        if not isinstance(note, AudioNote):
            return False
        octave = int(self.name[0])
        dest_octave = int(note.name[0])
        letter = self.name[1]
        dest_letter = note.name[1]
        sharp = len(self.name) > 2 and self.name[2] == '#'
        dest_sharp = len(note.name) > 2 and note.name[2] == '#'
        ret = 0
        if octave == dest_octave:
            ret = ord(dest_letter) - ord(letter)
        elif octave < dest_octave:  # fixme not accurate
            while octave != dest_octave:
                ret += 12
                octave += 1
            ret += ord(dest_letter) - ord(letter)
        else:
            while octave != dest_octave:
                ret -= 12
                octave -= 1
            ret += ord(dest_letter) - ord(letter)
        if sharp:
            ret -= 1
        if dest_sharp:
            ret += 1
        return ret

    def __str__(self):
        return self.name


class ChordNote(Note):
    """
    A list of notes that are played asynchronously
    """

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
    """
    A list of notes that are played in order
    """

    def play(self):
        for note in self:
            note.play()

    def distances(self):
        if len(self) < 2:
            return []
        ret = []
        for i in range(len(self) - 1):
            ret.append(self[i].distance(self[i + 1]))
        return ret

    def similarity(self, melody):
        return SequenceMatcher(None, self.distances(), melody.distances()).ratio()

    def __str__(self):
        ret = ""
        for item in self:
            ret += str(item)
        return ret


class ParallelMelody(Melody):
    """
    A list of melodies that are played asynchronously
    """

    def play(self):
        threads = []
        for melody in self:
            thread = Thread(target=melody.play)
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

    def __str__(self):
        ret = ""
        for melody in self:
            ret += str(melody)
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

    mel = ParallelMelody([m1, m2])
    while True:
        mel.play()
