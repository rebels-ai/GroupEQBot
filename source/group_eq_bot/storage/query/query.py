from elasticsearch_dsl import UpdateByQuery, Search, Q
from storage.connectors.connector import connection


def update_query(query, index_name: str, doc_type, source, params):

    ubq = UpdateByQuery(using=connection, index=index_name, doc_type=doc_type).query(query).script(source=source, params=params)
    
    ubq.execute()

def find_query(query, index_name: str, doc_type):
    s = Search(using=connection, index=index_name, doc_type=doc_type).query(query)
    try:
        r = s.execute()

    except Exception as error:
        r = []
        print(error)
    return r

def search_in_existing_index(query, index_name: str, doc_type):
    s = Search(using=connection, index=index_name, doc_type=doc_type).query(query)
    r = s.execute()
    print(r)
    return r
