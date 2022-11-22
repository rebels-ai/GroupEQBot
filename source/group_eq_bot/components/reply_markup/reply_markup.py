from typing import Any

from dataclasses import dataclass, field
from telegram import InlineKeyboardMarkup

@dataclass
class ReplyMarkup:
    """ Interface, which represents a custom object with reply option. """

    object: Any = field(init=True)
    
    def __post_init__(self):
        return InlineKeyboardMarkup(self.object)