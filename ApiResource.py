import requests
import openrouteservice

class Api_data():
    def __init__(self, params):
        self.client = openrouteservice.Client(key='API_KEY')
        self.params = params 

    def get_coordinates(self):
        coordinates = []
        for address in self.params:
            coordenadas = self.client.pelias_search(text=address)
            latitude = coordenadas['features'][0]['geometry']['coordinates'][1]
            longitude = coordenadas['features'][0]['geometry']['coordinates'][0]
            coordinates.append((longitude, latitude))
        return coordinates
        
    def get_route_data(self):
        self.coord_locations = self.get_coordinates()
        routes = self.client.directions(coordinates=[self.coord_locations[0], self.coord_locations[1]],
                                        profile='driving-car', format='geojson', radiuses=[35000, 35000])
        data = routes['features'][0]['properties']['segments'][0]
        return data