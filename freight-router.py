import requests
import csv

class Bot:
    def __init__(self, start, data_base):
        self.start_address = start
        self.url = 'http://dev.virtualearth.net/REST/v1/Routes/Driving'
        self.api_key = 'AqtlR0sr6MB5szBNcslOPgWQOZ115GlrgGLZ29GlNiRQ6y_SH3oO-YIjZyb2S3fX'
        self.db_address = []
        self.address_route = [start]
        self.read_db(data_base)
        self.address = None
        self.best_address = None


    def read_db(self, data_base):
        with open(data_base, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.db_address.append(row[0])

    def get_response_data(self):
        params = {
            'wp.0': self.start_address,
            'wp.1': self.address,
            'key': self.api_key,
            'routeAttributes': 'routePath'
        }
        self.response = requests.get(self.url, params=params)
        data = self.response.json()
        resources = data['resourceSets'][0]['resources']
        self.request = resources[0]

    def get_best_time(self):
        if self.distance < self.minor_distance and self.duration_hour < self.minor_time:
            self.minor_distance = self.distance
            self.minor_time = self.duration_hour
            self.best_address = self.address

    def log_request(self):
        len_msm = len(f"{self.start_address} to {self.address}")
        print("=" * len_msm)
        print(f"{self.start_address} to {self.address}")
        print(f'Distance: {self.distance:.2f} Km')
        print(f'Time: {self.duration_hour:.2f} hours')

    def get_time_distance(self):
        self.minor_distance = float('inf')
        self.minor_time = float('inf')
        for self.address in self.db_address:
            if self.address == self.start_address:
                continue
            if self.address in self.address_route:
                continue
            self.get_response_data()
            if self.response.status_code == 200:
                self.distance = self.request['travelDistance']
                self.duration_hour = self.request['travelDuration'] / 3600
                self.get_best_time()
                self.log_request()
                
    def get_route(self):
        for i in range(len(self.db_address)):
            self.get_time_distance()
            self.start_address = self.best_address
            self.address_route.append(self.best_address)
                   
    def execute(self):
        self.get_route()
        for i in self.address_route:
            print(i)
       

obj = Bot('Av. Nereu Ramos 1270 - Presidente Médici Chapecó SC', "endereco.csv")
obj.execute()
