#industry standard for studying graphs
import networkx as nx

class CarbonEngine:
    def __init__(self):

        #Data taken from GHG Protocol (grams of CO2 per metric ton per km)
        #Simplifying this to g per kg per km
        self.factors ={
            "Cargo Ship" : 0.012,
            "Rail" : 0.025,
            "Electric Truck" : 0.035,
            "Diesel Truck" : 0.105,
            "Air Freight" : 0.502
        }

    def run_study (self, weight, route_data):

        #route_data: list of dicts [{'from': 'A', 'to': 'B', 'dist': 100, 'mode': 'Rail'}]
        G = nx.DiGraph()        #Initialising empty directed graph (direction from point A to B is specific)
        total_carbon = 0

        #Loops at every leg (segment of the journey)
        for leg in route_data:

            # Formula: Weight * Distance * Emission Factor
            carbon_val = weight*leg['dist']*self.factors[leg['mode']]
            total_carbon += carbon_val
    
            G.add_edge(leg['from'], leg['to'], 
                       mode = leg['mode'],
                       carbon=round(carbon_val,2),
                       dist=leg['dist'])
        
        return G, round(total_carbon,2)     #Rounding to 2 decimal places for clean data