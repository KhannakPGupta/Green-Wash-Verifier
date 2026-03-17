import networkx as nx
from climatiq_service import get_transport_emissions

class CarbonEngine:
    #Expects the total weight of the cargo and a list of journey segments
    def run_study(self,weight,route_data):
        G=nx.DiGraph()      #To create directed graph between two points
        total_carbon=0

        for leg in route_data:
            #Calls Climatiq API and passes transport mode, distance for a specific leg and total weight
            emissions = get_transport_emissions(
                leg["mode"],
                leg["dist"],
                weight
            )

        total_carbon += emissions

        #Draws a line in network map between from and to locations
        G.add_edge(
                leg["from"],
                leg["to"],
                mode=leg["mode"],
                carbon=round(emissions,2),
                dist=leg["dist"]
            )
        
        return G, round(total_carbon,2)

        

