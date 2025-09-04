from dotenv import load_dotenv
load_dotenv()

from load_data import LoadData
from analyze import Analyze
from server import server

import time
import os
import uvicorn
import threading
import elastic_conn


class Main():

    def run(self):
        try:
            server_thread = threading.Thread(target=self.start_server, daemon=True)
            server_thread.start()

            csv_data = LoadData.read_csv_file()
            weapons = LoadData.read_txt_file()

            elastic_conn.initialize()
            elastic_conn.insert_data(csv_data)

            elastic_data = elastic_conn.get_all_data()
            analyzer = Analyze(weapons, elastic_data)
            analyzer.start()

            while True:
                time.sleep(60)

        except Exception as e:
            print(str(e))
            return str(e)

    def start_server(self):
        uvicorn.run(server, host=os.getenv("HOST"))

if __name__ == "__main__":
    Main().run()
