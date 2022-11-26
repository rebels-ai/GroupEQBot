import logging
from utilities.configurations_constructor.constructor import Constructor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def define_warning_logger() -> None:
    """ Method, which writes logs of warning level to machine, the system is running. """

    _directory = Constructor().configurations.bot.logging.directory
    _filename = Constructor().configurations.bot.logging.warning_file_name

    writer = logging.FileHandler(f'{_directory}/{_filename}')
    writer.setLevel(logging.WARNING)
    logger.addHandler(writer)

    return


def define_info_logger() -> None:
    """ Method, which writes logs of info level to machine, the system is running. """

    _directory = Constructor().configurations.bot.logging.directory
    _filename = Constructor().configurations.bot.logging.info_file_name

    writer = logging.FileHandler(f'{_directory}/{_filename}')
    writer.setLevel(logging.INFO)
    logger.addHandler(writer)

    return


