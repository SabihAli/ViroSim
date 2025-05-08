import random
avg = 0
count = 0
age_brackets = [
    (0, 4),  # toddlers
    (5, 17),  # children
    (18, 35),  # young adults
    (36, 60),  # adults
    (61, 80),  # seniors
    (81, 110)  # elderly
]

# Lower weights for less common age groups
weights = [
    5,  # toddlers
    15,  # children
    40,  # young adults
    25,  # adults
    10,  # seniors
    5  # elderly
]

def generate_age():
    chosen_bracket = random.choices(age_brackets, weights=weights, k=1)[0]
    return random.randint(chosen_bracket[0], chosen_bracket[1])

def generate_health_factor(lower_bias):
    return random.random() ** lower_bias


def generate_biased_bool(true_bias):
    return random.choices([True, False], weights=[true_bias, 1 - true_bias])[0]

def generate_recovery_time(node_data):
    global avg
    global count
    age_factor = (node_data.age / 110) ** 2
    health_factor = node_data.health_factor
    multiplier = (2 * age_factor + health_factor) / 3
    return 3 + (11 * multiplier)
