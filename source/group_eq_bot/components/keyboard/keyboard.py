from typing import List

from dataclasses import dataclass, field
from components.button.url_button import UrlButton

@dataclass
class Keyboard:
    """ Interface, which represents entity, which holds arbitrary number of buttons. """

    buttons: List[UrlButton] = field(init=True)

    def __post_init__(self):
        return [self.buttons]