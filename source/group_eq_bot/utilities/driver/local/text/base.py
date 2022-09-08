from pathlib import Path


class BaseTextReader:

    def open(path_to_read: Path) -> str:
        """  """
        with open(path_to_read, 'rt') as file:
            context = file.read()

        return context

