from elastic_conn import select_by_query

class RequestsController():

    def select_antisemic_with_weapon_docs():
        query = {
            "query" : {
                "bool" : {
                    "must" : [
                        {"term" : {"Antisemitic" : 1}},
                        {"exists" : {"field" : "Weapons" }}
                    ]
                }
            }  
        }
        return select_by_query(query)
    
    # select docs with tow or more weapons
    def select_docs_with_weapons():
        query = {
            "query" : {
               "script": {
                   "script" : {
                       "source" : "doc['Weapons'].size() >= 2",
                       "lang" : "painless"
                   }
               }
            }  
        }
        return select_by_query(query)