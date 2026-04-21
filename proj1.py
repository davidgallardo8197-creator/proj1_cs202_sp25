#complete your tasks in this file
import sys
import math
from typing import List
from dataclasses import dataclass

sys.setrecursionlimit(10**6)


@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float


@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str


@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float


# Example data
tokyo_rect = GlobeRect(35.5, 35.9, 139.5, 140.0)
tokyo = Region(tokyo_rect, "Tokyo", "other")
tokyo_condition = RegionCondition(tokyo, 2025, 14000000, 70000000.0)

paris_rect = GlobeRect(48.7, 49.0, 2.2, 2.5)
paris = Region(paris_rect, "Paris", "other")
paris_condition = RegionCondition(paris, 2025, 2100000, 10000000.0)

pacific_rect = GlobeRect(10.0, 20.0, -150.0, -140.0)
pacific = Region(pacific_rect, "Pacific Region", "ocean")
pacific_condition = RegionCondition(pacific, 2025, 0, 1000.0)

calpoly_rect = GlobeRect(35.1, 35.5, -120.9, -120.4)
calpoly = Region(calpoly_rect, "Cal Poly Area", "other")
calpoly_condition = RegionCondition(calpoly, 2025, 120000, 500000.0)

region_conditions = [
    tokyo_condition,
    paris_condition,
    pacific_condition,
    calpoly_condition
]


def emissions_per_capita(rc: RegionCondition) -> float:
    """
    Returns emissions per person.
    """
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate / rc.pop


def area(gr: GlobeRect) -> float:
    """
    Returns area of a globe rectangle in square kilometers.
    """
    r = 6378.1

    phi1 = math.radians(gr.lo_lat)
    phi2 = math.radians(gr.hi_lat)
    lam1 = math.radians(gr.west_long)
    lam2 = math.radians(gr.east_long)

    delta_lambda = lam2 - lam1
    if delta_lambda < 0:
        delta_lambda += 2 * math.pi

    return (r ** 2) * abs(delta_lambda) * abs(math.sin(phi2) - math.sin(phi1))


def emissions_per_square_km(rc: RegionCondition) -> float:
    """
    Returns emissions per square kilometer.
    """
    rect_area = area(rc.region.rect)
    if rect_area == 0:
        return 0.0
    return rc.ghg_rate / rect_area


def density(rc: RegionCondition) -> float:
    """
    Returns population density.
    """
    rect_area = area(rc.region.rect)
    if rect_area == 0:
        return 0.0
    return rc.pop / rect_area


def densest(rc_list: List[RegionCondition]) -> str:
    """
    Returns the name of the region with the highest population density.
    Assumes rc_list is not empty.
    """
    if len(rc_list) == 1:
        return rc_list[0].region.name

    rest_name = densest(rc_list[1:])
    first = rc_list[0]

    if first.region.name == rest_name:
        rest_region = first
    else:
        rest_region = find_region_by_name(rc_list[1:], rest_name)

    if density(first) >= density(rest_region):
        return first.region.name
    return rest_name


def find_region_by_name(rc_list: List[RegionCondition], name: str) -> RegionCondition:
    """
    Finds and returns the RegionCondition with the given name.
    Assumes it exists in the list.
    """
    if rc_list[0].region.name == name:
        return rc_list[0]
    return find_region_by_name(rc_list[1:], name)


def growth_rate(terrain: str) -> float:
    """
    Returns annual population growth rate based on terrain.
    """
    if terrain == "ocean":
        return 0.0001
    if terrain == "mountains":
        return 0.0005
    if terrain == "forest":
        return -0.00001
    return 0.0003


def project_population(pop: int, rate: float, years: int) -> int:
    """
    Projects population forward recursively.
    """
    if years == 0:
        return pop
    return project_population(int(pop * (1 + rate)), rate, years - 1)


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    """
    Returns a new projected RegionCondition after a number of years.
    """
    rate = growth_rate(rc.region.terrain)
    new_pop = project_population(rc.pop, rate, years)

    if rc.pop == 0:
        new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(
        region=rc.region,
        year=rc.year + years,
        pop=new_pop,
        ghg_rate=new_ghg
    )