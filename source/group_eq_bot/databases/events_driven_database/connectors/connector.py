from elasticsearch_dsl.connections import connections

from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

# Fetch bot configuration with hydra compose api
# https://hydra.cc/docs/advanced/compose_api/
initialize(version_base="1.2", config_path="../../../configurations", job_name="database_host")
configurations = compose(config_name="configuration")
GlobalHydra.instance().clear()


host = configurations.events_driven_database.which_host_to_use.host
connection = connections.create_connection(hosts=[host])
