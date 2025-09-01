from fastapi import FastAPI
from requests_controller import RequestsController

server = FastAPI()

@server.get('/antisemic-docs')
def get_antisemic_tweets():
    try:
        data = RequestsController.select_antisemic_with_weapon_docs()
        if data['hits']['total']['value'] == 0:
            return {"response" : "Data not found"}
        else:
            return data['hits']['hits']
    except Exception as e:
        print(str(e))
        return {"Error" : str(e)}

@server.get('/weapons-docs')
def get_antisemic_tweets():
    try:
        data = RequestsController.select_docs_with_weapons()
        if data['hits']['total']['value'] == 0:
            return {"response" : "Data not found"}
        else:
            return data['hits']['hits']
    except Exception as e:
        print(str(e))
        return {"Error" : str(e)}

