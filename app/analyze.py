import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from elastic_conn import add_mapping_field, add_new_field, delete_doc_by_query

class Analyze():

    def __init__(self, weapons, data):
        nltk.download('vader_lexicon')
        self.analyzer = SentimentIntensityAnalyzer()
        self.weapons = weapons
        self.data = data
        
    def start(self):
        try:
            self.add_emotion()
            self.add_weapons()
            self.remove_docs()
            print("Finish analyze.")
        except Exception as e:
            print("Error: ", str(e))
            return str(e)
        
    def find_weapons(self, text):
        weapons_list = []
        words = text.split()
        for weapon in self.weapons:
            if weapon in words:
                weapons_list.append(weapon)
        return weapons_list

    def find_emotion(self, text):
        score = self.analyzer.polarity_scores(text)
        compound = score['compound']
        if 0.5 < compound <= 1:
            return 'positive'
        elif -0.49 <= compound <= 0.49:
            return 'neutral'
        elif -1 <= compound < -0.5:
            return 'negative'
         
    def add_weapons(self):
        print("start add weapons")
        new_map_field = {'Weapons' : { 'type' : 'keyword'}}
        add_mapping_field(new_map_field)

        data_result = {}
        for doc in self.data:
            weapons = self.find_weapons(doc['_source']['text'])
            data_result[doc['_id']] = {'Weapons' : weapons}
        add_new_field(data_result)
        print("weapons added.")
        # for hit in self.data['hits']['hits']:
        #     weapons = self.find_weapons(hit['_source']['text'])
        #     data_result[hit['_id']] = {'Weapons' : weapons}

        # for key, val in data_result.items():
        #     add_new_field(key, val)
        
        
        
    def add_emotion(self):
        print("start add emotion")
        new_map_field = {'Emotion' : { 'type' : 'keyword'}}
        add_mapping_field(new_map_field)
        
        data_result = {}
        for doc in self.data:
            emotion = self.find_emotion(doc['_source']['text'])
            data_result[doc['_id']] = {'Emotion' : emotion}
        add_new_field(data_result)
        print("emotion added.")
        # for hit in self.data['hits']['hits']:
        #     emotion = self.find_emotion(hit['_source']['text'])
        #     data_result[hit['_id']] = {'Emotion' : emotion}
        
        # for key, val in data_result.items():
        #     add_new_field(key, val)


    # remove non antisemite docs, with no weapons and positive or netural emotion
    def remove_docs(self):
        query = {
            "query" : {
                "bool" : {
                    "must" : [
                        { "term" : {"Antisemitic": 0}},
                        { "terms" : { "Emotion" : ['positive', 'neutral']}}
                    ],
                    "must_not" : [
                        {
                            "exists" : { "field" : "Weapons"}
                        }
                    ]
                }
            }
        }
        delete_doc_by_query(query)