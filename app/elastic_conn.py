from elasticsearch import Elasticsearch
import os


es = Elasticsearch(os.getenv('ES_PATH'))
index_name = os.getenv('ES_INDEX')

def initialize():
    create_index()
    add_mapping()

def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

def delete_index():
    es.indices.delete(index=index_name)

def add_mapping(): 
    mapping = {
        'properties': {
            'TweetID': {
                'type': 'keyword',
                'ignore_above': 256
            },
            'CreateDate': {
                'type': 'keyword',
            },
            'Antisemitic': {
                'type': 'integer',
            },
            'text': {
                'type': 'text',
            },
        }
    } 
    es.indices.put_mapping(index=index_name, body=mapping)  

def insert_data(doc_list):
    for doc in doc_list:
        es.index(index=index_name, body=doc)

def add_new_field(doc_id, dict_data):
    es.update(
        index=index_name,
        id=doc_id,
        doc=dict_data
    )

def add_mapping_field(dict_mapp):
    es.indices.put_mapping(
        index=index_name,
        body={"properties": dict_mapp}
    )

def get_all_data():
    query = {
        "query": {
            "match_all": {}
        },
        'size': 10000
    }
    results = es.search(index=index_name, body=query)
    return results

def get_data_by_field(field):
    query = {
        "_source" : [field],
        "query": {
            "match_all": {},
        },
        'size': 10000
    }
    results = es.search(index=index_name, body=query)
    return results

def delete_doc_by_query(query):
    try:
        responce = es.delete_by_query(
            index=index_name,
            body=query,
            wait_for_completion=True
        )
        print(responce)
    except Exception as e:
        print(str(e))
        return e

def select_by_query(query):
    try:
        response = es.search(index=index_name, body=query)
        return response
    except Exception as e:
        print(e)
        return str(e)
