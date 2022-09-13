from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

from dataclasses import dataclass, field

from omegaconf import DictConfig


@dataclass
class Constructor:
    """
    Class stands for main interface to build configurations dict
    based on configurations yaml file.

    Notes:
        Fetch bot configuration with hydra compose api: https://hydra.cc/docs/advanced/compose_api/

    Usage:
        to get access to the configurations:
            Constructor().configurations.<bot>...
            Constructor().configurations.<events_database>...
    """

    _HYDRA_VERSION = '1.2'
    _CONFIGURATIONS_FOLDER_NAME = 'configurations'

    _CONFIGURATIONS_PATH = f'../../{_CONFIGURATIONS_FOLDER_NAME}'
    _CONFIGURATIONS_FILE_NAME = 'configuration'

    configurations: DictConfig = field(init=False)

    def _initialize_hydra(self):
        """ Helper method, which initializes Hydra and add the config_path to the config search path. """
        initialize(version_base=self._HYDRA_VERSION, config_path=self._CONFIGURATIONS_PATH)

    def _compose_configurations(self):
        """ Helper method, which overrides the hydra instance. """
        self.configurations = compose(config_name=self._CONFIGURATIONS_FILE_NAME, return_hydra_config=True)
        GlobalHydra.instance().clear()

    def __post_init__(self):
        self._initialize_hydra()
        self._compose_configurations()
