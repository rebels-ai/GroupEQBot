from dataclasses import dataclass, field
from telegram import InlineKeyboardButton


@dataclass
class UrlButton:
    """ Interface, which represents clickable UrlButton. """

    text: str = field(init=True)
    url: str = field(init=True)

    def __post_init__(self):
        return InlineKeyboardButton(text=self.text, url=self.url)