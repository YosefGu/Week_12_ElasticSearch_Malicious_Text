from fastapi import FastAPI, Body
from requests_controller import RequestsController
from elastic_conn import get_all_data, select_by_query


server = FastAPI()

@server.get('/all-data')
def all_data():
    try:
        data = get_all_data()
        return data
        # if data['hits']['total']['value'] == 0:
        #     return {"response" : "Data not found, no data result match the query."}
        # else:
        #     return data['hits']['hits']
    except Exception as e:
        print(str(e))
        return {"Error" : str(e)}

@server.get('/antisemic-docs')
def get_antisemic_tweets():
    try:
        data = RequestsController.select_antisemic_with_weapon_docs()
        return data
        # if data['hits']['total']['value'] == 0:
        #     return {"response" : "Data not found, no data result match the query."}
        # else:
        #     return data['hits']['hits']
    except Exception as e:
        print(str(e))
        return {"Error" : str(e)}

@server.get('/weapons-docs')
def get_antisemic_tweets():
    try:
        data = RequestsController.select_docs_with_weapons()
        return data
        # if data['hits']['total']['value'] == 0:
        #     return {"response" : "Data not found, no data result match the query."}
        # else:
        #     return data['hits']['hits']
    except Exception as e:
        print(str(e))
        return {"Error" : str(e)}

@server.post('/search-query')
def execute_search_query(query: dict = Body(...)):
    return select_by_query(query)
