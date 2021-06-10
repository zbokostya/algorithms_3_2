import random

from collections import OrderedDict
from itertools import islice

POPULATION_SIZE = 3000
MIN_VALUE = -200
MAX_VALUE = 200
NUM_ITEMS_FOR_SELECTION = 1000
NUM_ITEMS_FOR_MUTATION = 500
NUM_OF_SUITABLE_DESCEDANTS = 200

MUTATION_PROBABILITY_FOR_UNSUITABLE = 0.25
DESCEDANT_PROBABILITY = 0.25

TARGET_VALUE = 40


def target_function(u, w, x, y, z):
    return abs(
        (u ** 2 * w * x ** 2 * y ** 2) + (u ** 2 * x ** 2 * z ** 2) + (w ** 2 * x * y ** 2 * z) + (y * z) + (
                w * x * z ** 2) - TARGET_VALUE
    )


def generate_item(min_value, max_value):
    return [random.randint(min_value, max_value) for _ in ['u', 'w', 'x', 'y', 'z']]


def create_initial_population(population_size: int, min_value: int, max_value: int):
    population = []
    for index in range(population_size):
        item = generate_item(min_value, max_value)
        population.append(item)
    return population


def sum(arr):
    rez = 0
    for i in arr:
        rez += i
    return rez


def perform_proportional_selection(population, num_items_for_selection, num_items_for_mutation, target_function):
    rez = dict()
    sample = random.sample(population, num_items_for_selection)
    prop = []
    for item in sample:
        func = target_function(*item) - TARGET_VALUE
        if func == 0:
            prop.append(0)
        else:
            prop.append(1 / func)

    if sum(prop) < 10E-6:
        gen = islice(sample, 0, num_items_for_mutation)
    else:
        gen = random.choices(sample, prop, k=num_items_for_mutation)

    for item in gen:
        rez[target_function(*item)] = item

    return list(OrderedDict(rez).values())


def perform_homogeneous_crossing_for_two_elements(first_item, second_item):
    new_item = [
        random.choice([coordinate1, coordinate2]) for coordinate1, coordinate2 in zip(first_item, second_item)
    ]
    return new_item


def perform_homogeneous_crossing(selection, descendants_size):
    # random selection of 2
    descendants = [
        perform_homogeneous_crossing_for_two_elements(random.choice(selection), random.choice(selection))
        for _ in range(descendants_size)
    ]
    return descendants


def should_perform_coordinate_mutation(mutation_probability):
    return random.random() < mutation_probability


def perform_mutation(
        selection, num_of_suitable_descendants, mutation_probability_for_unsuitable
):
    # mutate unsuitable with p
    for item in selection[num_of_suitable_descendants:]:
        for index, coordinate in enumerate(item):
            if should_perform_coordinate_mutation(mutation_probability_for_unsuitable):
                item[index] = random.randint(MIN_VALUE, MAX_VALUE)
    return selection


def perform_descendants_substitution(selection, population_size, target_function):
    sample = [(item, target_function(*item)) for item in selection]
    sample.sort(key=lambda x: x[1])
    sample[len(sample) - int(len(sample) * DESCEDANT_PROBABILITY):] = sample[int(len(sample) * DESCEDANT_PROBABILITY):]
    sample = [item[0] for item in sample]
    rez = dict()
    for item in sample:
        rez[target_function(*item)] = item

    return list(OrderedDict(rez).values())


def run_genetic_algorithm(
        population_size, min_value, max_value, num_items_for_selection, num_items_for_mutation, target_function,
        num_of_suitable_descedants, mutation_probability_for_unsuitable
):
    initial_population = create_initial_population(population_size, min_value, max_value)
    iteration = 0

    while True:
        selection = perform_proportional_selection(
            initial_population, num_items_for_selection, num_items_for_mutation, target_function
        )
        descendants = perform_homogeneous_crossing(selection, 2 * population_size)
        descendants = perform_mutation(
            descendants,
            num_of_suitable_descedants,
            mutation_probability_for_unsuitable
        )
        selection = perform_descendants_substitution(
            descendants, population_size, target_function
        )

        print(
            f"MIN of target values: {selection[0]} = {target_function(*selection[0]) + TARGET_VALUE}")

        result = []
        for item in selection:
            if target_function(*item) == 0:
                result.append(item)
        if result:
            return result

        if iteration == 10000:
            return None
        iteration += 1


population = create_initial_population(POPULATION_SIZE, MIN_VALUE, MAX_VALUE)

selection = perform_proportional_selection(population, NUM_ITEMS_FOR_SELECTION, NUM_ITEMS_FOR_MUTATION, target_function)

selection = perform_mutation(
    selection,
    NUM_OF_SUITABLE_DESCEDANTS,
    MUTATION_PROBABILITY_FOR_UNSUITABLE
)

result = run_genetic_algorithm(
    POPULATION_SIZE,
    MIN_VALUE,
    MAX_VALUE,
    NUM_ITEMS_FOR_SELECTION,
    NUM_ITEMS_FOR_MUTATION,
    target_function,
    NUM_OF_SUITABLE_DESCEDANTS,
    MUTATION_PROBABILITY_FOR_UNSUITABLE
)

print()
print("Target Value:", TARGET_VALUE)
print(result)
