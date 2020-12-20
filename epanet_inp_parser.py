import wntr
from networkx.readwrite import json_graph
import json

if __name__ == '__main__':
    network = wntr.network.WaterNetworkModel('network_test.inp')
    graph = network.get_graph()

    with open("static/network_test.json", 'w') as json_file:
        json_file.write(json.dumps(json_graph.node_link_data(graph)))
