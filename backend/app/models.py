
""" These variables are universal factors which will increase/decrease
EVERYONE'S infection probability """
from enum import Enum

season = "winter"
lockdown = True


class InfectionStatus(Enum):
    """
        Enum class to represent the infection status of a node.

        Attributes:
            SUSCEPTIBLE (str): A node that is not yet infected but is at risk.
            INFECTED (str): A node that is currently infected.
            RECOVERED (str): A node that has recovered from the infection.
            DECEASED (str): A node that has died due to the infection.
    """

    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"
    DECEASED = "D"


class Node:
    """
    Each node of the graph will represent an individual person.

    Attributes:
        infection_status (InfectionStatus): The infection status of the individual

        death_probability (float): The probability of the individual dying due to the disease, MUST be infected. Updates on each tick.

        age (int): The age of the individual (Older people may be more susceptible)

        health_factor (float): Factor which increases susceptibility due to past health conditions.
        (MIN: 0, MAX: 1) (normalized)

        mask_usage (bool): Determines whether the individual wears a mask or not.

        vax_status (bool): Determines whether the individual is vaccinated or not.

        superspreader (bool): Determines whether the individual is a superspreader or not
    """

    def __init__(self, infection_status, age, health_factor, mask_usage, vax_status, superspreader):
        self.infection_status = infection_status
        self.infected_tick = None
        self.recovery_tick = None
        self.recovery_time = None
        self.death_probability = None
        self.age = age
        self.health_factor = health_factor
        self.mask_usage = mask_usage
        self.vax_status = vax_status
        self.superspreader = superspreader






class Edge:
    """
    Each edge of the graph will represent the relationship between two individuals.

    The infection probability is an attribute associated with EDGES, NOT nodes.

    Attributes:
        node_one (Node): First node/individual associated with the edge

        node_two (Node): Second node/individual associated with the edge

        rs_strength (float): represents the strength of the relationship
        (MIN: 0, MAX: 1) (normalized)

        avg_contact_freq (float): How many times the two nodes meet PER DAY on average
        (MIN: 0, MAX: 5)

        avg_interact_duration (float): Average duration (in hours) the two nodes interact for.
        (MIN: 0, MAX: 24)

        physical_dist (float): Average physical distance b/w the two nodes during interaction
        (MIN: 0, MAX: 1) (normalized)

        indoor_ratio (float): Ratio of indoor interactions to total interactions b/w the two individuals
        (MIN: 0, MAX: 1) (normalized)

        infection_prob (float): The probability of infecting adjacent node
        (MIN: 0, MAX: 1)
    """

    def __init__(self, node_one, node_two, rs_strength, contact_freq, avg_interact_duration, indoor_ratio, physical_dist):
        self.node_one = node_one
        self.node_two = node_two
        self.rs_strength = rs_strength
        self.contact_freq = contact_freq
        self.avg_interact_duration = avg_interact_duration
        self.physical_dist = physical_dist
        self.indoor_ratio = indoor_ratio
        self.infection_prob = 1 / (1 + abs(node_two.age - node_one.age))
