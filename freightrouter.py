from ApiResource import Api_data
import csv

class Router:
    def __init__(self, start, data_base):
        self.start_address = start
        self.address_route = [start]
        self.db_address = []
        self.address = None
        self.best_address = None
        self.data_base = data_base
        
    def read_db(self, data_base):
        with open(data_base, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.db_address.append(row[0])

    def get_response_data(self):
        params = [
            self.start_address, 
            self.address,
        ]
        self.request = Api_data(params).get_route_data()

    def get_best_time(self):
        self.distance = self.request['distance']
        self.duration_hour = self.request['duration'] / 3600
        
        if self.distance < self.minor_distance and self.duration_hour < self.minor_time:
            self.minor_distance = self.distance
            self.minor_time = self.duration_hour
            self.best_address = self.address

    def log_request(self):
        len_msm = len(f"{self.start_address} to {self.address}")
        print("-" * len_msm)
        print(f"{self.start_address} to {self.address}")
        print(f'Distance: {self.distance:.2f} Km')
        print(f'Time: {self.duration_hour:.2f} hours')
        print("-" * len_msm)

    def get_time_distance(self):
        self.minor_distance = float('inf')
        self.minor_time = float('inf')
        for self.address in self.db_address:
            if self.address == self.start_address:
                continue
            if self.address in self.address_route:
                continue
            
            self.get_response_data()
            self.get_best_time()
            self.log_request()
                
    def get_route(self):
        for i in range(len(self.db_address)):
            self.get_time_distance()
            self.start_address = self.best_address
            self.address_route.append(self.best_address)
                   
    def execute(self):
        self.read_db(self.data_base)
        self.get_route()
           
