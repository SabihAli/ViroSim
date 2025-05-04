import random


def get_normalized_factor(bias):
    return random.random() ** bias

def get_interact_duration():
    return get_normalized_factor(2) * 24

def get_contact_freq():
    return get_normalized_factor(1.25) * 5

def get_physical_dist():
    return get_normalized_factor(1.25)

def get_indoor_ratio():
    return get_normalized_factor(0.75)

def get_rs_strength(age_one, age_two):
    duration = get_interact_duration()
    frequency = get_contact_freq()
    distance = get_physical_dist()
    indoor_ratio = get_indoor_ratio()
    age_diff_factor = 1/(1 + abs(age_two - age_one))

    return (2 * duration + frequency + distance + indoor_ratio + 3 * age_diff_factor) / 58


def get_age_factor(age, peak=26.5, width=10):
    """
        Returns a vitality factor between 0 and 1, highest around peak age,
        and lower for toddlers and the elderly.

        Parameters:
            - age: Age of the node (integer)
            - peak: Center of high vitality (default: middle of 18-35)
            - width: Controls how quickly it falls off

        Returns:
            - A float between 0 and 1
    """

    from math import exp

    return exp(-((age - peak) ** 2) / (2 * width ** 2))


def get_node_score(age, health_factor, mask_usage, vax_status, superspreader):
    """
        Returns normalized infection risk between 0 and 1.
    """

    age_factor = get_age_factor(age)

    # Average of age and health risk (each in [0, 1])
    risk = (age_factor + health_factor) / 2

    # 1 (normal) or 3 (superspreader)
    multiplier = 1 + 2 * superspreader

    # Mask reduces risk: 2 if worn, 1 if not
    mask_effect = 2 if mask_usage else 1

    # Vaccine reduces risk: 4 if vaccinated, 1 if not
    vax_effect = 4 if vax_status else 1

    # Final raw score [0, 3]
    raw_score = (risk * multiplier) / (mask_effect * vax_effect)

    # Normalize by max possible score (3.0) to clamp into [0,1]
    normalized_score = raw_score / 3.0

    return min(1.0, max(0.0, normalized_score))  # ensures strict [0,1]



def get_infection_prob(node_one, node_two):


    rs_strength = get_rs_strength(node_one.age, node_two.age)


    if node_one.infection_status != 'I' and node_two.infection_status != 'I':
        return 0

    if node_one.infection_status == 'D' or node_two.infection_status == 'D':
        return 0

    if node_one.infection_status == 'R' or node_two.infection_status == 'R':
        return 0


    node_one_score = get_node_score(node_one.age, node_one.health_factor, node_one.mask_usage, node_one.vax_status, node_one.superspreader)
    node_two_score = get_node_score(node_two.age, node_two.health_factor, node_two.mask_usage, node_two.vax_status, node_two.superspreader)


    return (node_one_score + node_two_score + 2 * rs_strength) / 4











