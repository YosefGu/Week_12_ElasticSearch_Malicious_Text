from elasticsearch import Elasticsearch, helpers
import os


es = Elasticsearch(os.getenv('ES_PATH'))
index_name = os.getenv('ES_INDEX')

def initialize():
    delete_index()
    create_index()
    add_mapping()

def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

def delete_index():
    if es.indices.exists(index=index_name):
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
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in doc_list
    ]
    helpers.bulk(es, actions)
    es.indices.refresh(index=index_name)

    # for index, doc in enumerate(doc_list):
    #     es.index(index=index_name, body=doc)
    #     if index > 100:
    #         break

def add_new_field(dict_data):
    actions = [
        {
            "_op_type": "update",
            "_index": index_name,
            "_id": doc_id,
            "doc": doc,
        } for doc_id, doc in dict_data.items()
    ]
    success, errors = helpers.bulk(es, actions)
    print("Number of successful updates:", success)
    print("Errors:", errors)
    es.indices.refresh(index=index_name)
    # es.update(
    #     index=index_name,
    #     id=doc_id,
    #     doc=dict_data
    # )

def add_mapping_field(dict_mapp):
    es.indices.put_mapping(
        index=index_name,
        body={"properties": dict_mapp}
    )

def get_all_data():
    results = helpers.scan(
        client=es,
        index=index_name,
        query={"query": {"match_all": {}}},
        _source=True
    )

    all_docs = list(results) 
    return all_docs
    # all_docs = [doc for doc in results]
    # return all_docs
    # query = {
    #     "query": {
    #         "match_all": {}
    #     },
    #     'size': 100
    # }
    # results = es.search(index=index_name, body=query)
    # return results

def get_data_by_field(field):
    query = {
        "_source" : [field],
        "query": {
            "match_all": {},
        },
        'size': 50000
    }
    results = es.search(index=index_name, body=query)
    return results

# def get_data_by_query(inner_query):
#     query = {inner_query}
#     return es.search(index=index_name, body=query)

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
