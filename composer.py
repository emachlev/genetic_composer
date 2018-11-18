import random

from notes import Melody, AudioNote, RestNote, ChordNote

CHROMOSOME_SIZE = 80  # Must be divisible by 4
POPULATION_SIZE = 10

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001

AVAILABLE_NOTES = {
    '0000': 'A',
    '0001': 'A#',
    '0010': 'B',
    '0011': 'C',
    '0100': 'C#',
    '0101': 'D',
    '0110': 'D#',
    '0111': 'E',
    '1000': 'F',
    '1001': 'F#',
    '1010': 'G',
    '1011': 'G#',
    '1100': 'R',  # Rest note
}

REPETITION_RATE = 0.4


def get_random_chromo():
    chromo = ""
    prev = ""
    for _ in range(CHROMOSOME_SIZE):
        if prev and random.uniform(0, 1) <= REPETITION_RATE:
            char = prev
        else:
            char = str(random.randint(0, 1))
        chromo += char
        prev = char
    return chromo


def validate_expression(exp):
    exp = exp.strip('R#')
    ret = ""
    for i, char in enumerate(exp):
        if not (char in ['B', 'E'] and (i < len(exp) - 1 and exp[i + 1] == '#')):
            ret += char
    return ret


def decode_chromo(chromo):
    ret = ""
    if len(chromo) % 4 != 0:
        return False
    for chunk in [str(chromo[i:i + 4]) for i in range(0, len(chromo), 4)]:
        if chunk in AVAILABLE_NOTES:
            ret += AVAILABLE_NOTES[chunk]
    return validate_expression(ret)


def get_melody_from_exp(exp):
    if not exp:
        return Melody()
    ret = Melody()
    for i, char in enumerate(exp):
        if char != 'R' and (i < len(exp) - 1 and exp[i + 1] == '#') and char != '#':
            ret.append(AudioNote(char + exp[i + 1]))
        elif char == 'R':
            ret.append(RestNote())
        elif char != '#':
            ret.append(AudioNote(char))
    return ret


def rate(population, fitnesses):
    for i in range(POPULATION_SIZE):
        melody = get_melody_from_exp(decode_chromo(population[i]))
        melody.play()
        act = input(str(melody) + ' - Rate (1-10) or any key to hear again: ')
        while not act.isdigit():
            melody.play()
            act = input(str(melody) + ' - Rate (1-10) or any key to hear again: ')
        fitnesses[i] = float(act)


def weighted_random_choice(choices):
    maxv = sum(choices.values())
    pick = random.uniform(0, maxv)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key


def select_two(fitnesses):
    i1 = weighted_random_choice(fitnesses)
    i2 = i1
    while i2 == i1:
        i2 = weighted_random_choice(fitnesses)
    return i1, i2


def crossover(population, chosen):
    if random.uniform(0, 1) <= CROSSOVER_RATE:
        chromo_1 = population[chosen[0]]
        chromo_2 = population[chosen[1]]
        point = int(random.randint(0, CHROMOSOME_SIZE) / 2)
        from_1 = chromo_1[point:]
        from_2 = chromo_1[point:]
        population[chosen[0]] = chromo_1[:point] + from_2
        population[chosen[1]] = chromo_2[:point] + from_1


def mutate(population, chosen):
    chromo_1 = list(population[chosen[0]])
    chromo_2 = list(population[chosen[1]])
    for i, char in enumerate(chromo_1):
        if random.uniform(0, 1) <= MUTATION_RATE:
            chromo_1[i] = '1' if char == 0 else '0'
    for i, char in enumerate(chromo_2):
        if random.uniform(0, 1) <= MUTATION_RATE:
            chromo_2[i] = '1' if char == 0 else '0'
    population[chosen[0]] = ''.join(chromo_1)
    population[chosen[1]] = ''.join(chromo_2)


def main():
    population = [get_random_chromo() for _ in range(POPULATION_SIZE)]
    fitnesses = {}
    generation = 1
    while True:
        rate(population, fitnesses)
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            selected = select_two(fitnesses)
            crossover(population, selected)
            mutate(population, selected)
            new_population.append(population[selected[0]])
            new_population.append(population[selected[1]])
        population = new_population
        generation += 1


if __name__ == '__main__':
    main()
