import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'laba_03'))
from models import TeamCompetition, IndividualCompetition
from base import Competition

def by_name(comp: 'Competition') -> str:
    return comp.name

def by_max_participants(comp: 'Competition') -> int:
    return comp.max_participants

def by_duration(comp: 'Competition') -> int:
    return comp.get_competition_duration()

def by_status_and_name(comp: 'Competition') -> tuple:
    status_order = {"Registration": 1, "In Progress": 2, "Completed": 3, "Cancelled": 4}
    return (status_order.get(comp.status, 99), comp.name)

def is_long_duration(comp: 'Competition') -> bool:
    return comp.get_competition_duration() > 2

def is_team_competition(comp: 'Competition') -> bool:
    return isinstance(comp, TeamCompetition)

def make_participants_filter(min_participants: int):
    def filter_fn(item: 'Competition') -> bool:
        return item.max_participants >= min_participants
    return filter_fn

def make_status_transition(new_status: str):
    def transition_fn(item: 'Competition') -> str:
        return f"{item.name}: {item.next_status()}"
    return transition_fn

def to_summary(comp: 'Competition') -> str:
    return f"{comp.name} ({comp.sport_type}) — {comp.status}"

def extract_location(comp: 'Competition') -> str:
    return comp.location

class StatusUpgradeStrategy:
    def __call__(self, item: 'Competition') -> 'Competition':
        item.next_status()
        return item

class FeeCalculationStrategy:
    def __call__(self, item: 'Competition') -> str:
        fee = item.calculate_organizer_fee()
        return f"{item.name}: взнос = {fee:.2f} руб."

class RegistrationMultiplierStrategy:
    def __call__(self, item: 'Competition') -> 'Competition':
        item._max_participants *= 2
        return item
