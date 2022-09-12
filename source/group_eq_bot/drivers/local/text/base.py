from pathlib import Path


class BaseTextReader:
    """ Reader for any kind of text files """

    @staticmethod
    def read(path_to_read: Path) -> str:
        """ Function, which reads the text from file at specified path """

        with open(path_to_read, 'rt') as file:
            context = file.read()

        return context
