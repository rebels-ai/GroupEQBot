from elasticsearch_dsl.connections import connections
from utilities.configurations_constructor.constructor import Constructor


host = Constructor().configurations.events_database.which_host_to_use.host
connection = connections.create_connection(hosts=[host])
