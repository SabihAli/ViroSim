import random
import math
from backend.app.models import InfectionStatus

avg = 0
count = 0

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
    age_diff_factor = 1 / (1 + abs(age_two - age_one))

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
    vax_effect = 3 if vax_status else 1

    # Final raw score [0, 3]
    raw_score = (risk * multiplier) / (mask_effect * vax_effect)

    # Normalize by max possible score (3.0) to clamp into [0,1]
    normalized_score = raw_score / 3.0

    return min(1.0, max(0.0, normalized_score))  # ensures strict [0,1]


def get_infection_prob(node_one_data, node_two_data):
    rs_strength = get_rs_strength(node_one_data.age, node_two_data.age)

    node_one_score = get_node_score(node_one_data.age, node_one_data.health_factor, node_one_data.mask_usage,
                                    node_one_data.vax_status, node_one_data.superspreader)
    node_two_score = get_node_score(node_two_data.age, node_two_data.health_factor, node_two_data.mask_usage,
                                    node_two_data.vax_status, node_two_data.superspreader)

    return ((node_one_score + node_two_score + 3 * rs_strength) / 5) ** 0.5


def get_death_prob(node_data, current_tick):
    infect_duration = current_tick - node_data.infected_tick
    age_score = node_data.age / 110

    # Infection duration factor: scales from 0 to 1 logarithmically for longer durations
    duration_factor = min(1.0, math.log1p(infect_duration) / math.log1p(30))

    """ Expression is [0,1]. Raised to power 10 to ensure death probability is very low. """
    return (0.35 * age_score + 0.4 * node_data.health_factor + 0.25 * duration_factor) ** 10


