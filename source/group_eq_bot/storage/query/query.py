from typing import Union, List

from elasticsearch_dsl import UpdateByQuery, Search
from elasticsearch_dsl.query import Query
from elasticsearch_dsl.response import Response

from storage.connectors.connector import connection


def update_query(query: Query, index_name: str, doc_type, source: str, params) -> None:
    """ Function, which partially updates document in specified index. 
        Source and params are the path and values for those changes. """

    update_task = UpdateByQuery(using=connection, 
                        index=index_name, 
                        doc_type=doc_type).query(query).script(source=source, params=params)
    update_task.execute()

def find_query(query, index_name: str, doc_type) -> Union[Response, List]:
    """ Function, which searches document in specified index """

    search_task = Search(using=connection, index=index_name, doc_type=doc_type).query(query)
    try:
        response = search_task.execute()
    except Exception as error:
        response = []
    return response

def search_in_existing_index(query, index_name: str, doc_type) -> Response:
    """ Function, which searches document in existing index """

    search_task = Search(using=connection, index=index_name, doc_type=doc_type).query(query)
    response = search_task.execute()
    return response
