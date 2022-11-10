import re 
from typing import List

def check_valid_roles(roles: str) -> bool:
    return _is_digit_str(roles) and _has_count_elements(roles, 4)

def check_valid_nick(nicks: List) -> bool:
    return len(nicks) == 10

def check_valid_nominations(nomitations: str, active_players: List  )-> bool:
    return _is_digit_str(nomitations) and _has_player_in_active_players(nomitations, active_players)


def _is_digit_str(text: str) -> bool:
    try:
        return bool(str_to_digit_list_int(text))
    except:
        return False  

def _has_count_elements(text: str, count: int) -> bool:
    return len(re.sub("[0-9]+", "", text)) + 1 == count 




def _has_player_in_active_players( text_players: str, active_players: List) -> bool:
    return set(str_to_digit_list_int(text_players)).issubset(active_players)


def str_to_digit_list_int(text : str) -> List[int]:
    return [int(x) for x in text.split()]