
class LoadData():

    @staticmethod
    def read_txt_file(file_path='/data/weapon_list.txt'):
        try: 
            with open(file_path, 'r') as f:
                data = f.read()
                print(data)
                return data
        except Exception as e:
            print(str(e))
            return e
        

LoadData.read_txt_file()
