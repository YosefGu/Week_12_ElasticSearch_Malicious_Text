import csv

class LoadData():

    @staticmethod
    def read_txt_file(file_path='data/weapon_list.txt'):
        try: 
            with open(file_path, 'r',  encoding='utf-8') as f:
                data = f.read().split()
                return data
        except Exception as e:
            print(str(e))
            return e
        
    @staticmethod
    def read_csv_file(file_path='data/tweets_injected.csv'):
        try: 
            with open(file_path, 'r',  encoding='utf-8') as f:
                data = csv.DictReader(f)
                return list(data)
        except Exception as e:
            print(str(e))
            return e
        

# LoadData.read_txt_file()
# LoadData.read_csv_file()
