from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class GameParams(DataClassJsonMixin):
    more_ability_cards: bool = False
    give_every_card_to_players: bool = False
    random_color: bool = False
    random_turn: bool = False
