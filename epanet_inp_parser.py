from epanettools.epanettools import EPANetSimulation
import json

EPANET_NODE_TYPES = {0: 'Junction', 1: 'Reservoir', 2: 'Tank'}
EPANET_LINK_TYPES = {0: 'CVPIPE', 1: 'Pipe',  2: 'Pump', 3: 'PRV', 4: 'PSV', 5: 'PBV', 6: 'FCV', 7: 'TCV', 8: 'GPV'}


class JsonNode(dict):
    def __init__(self, id_, type_):
        super().__init__()
        self.__setitem__("id", id_)
        self.__setitem__("type_", type_)


class JsonLink(dict):
    def __init__(self, source, target):
        super().__init__()
        self.__setitem__("source", source)
        self.__setitem__("target", target)


def write_json_file(graph_dict):
    with open("static/network_test.json", 'w') as json_file:
        json_file.write(json.dumps(graph_dict))


if __name__ == '__main__':
    network = EPANetSimulation('network_test.inp').network
    data_dict = {"nodes": [],
                 "links": []}
    nodes = network.nodes.store
    for n in nodes.values():
        json_node = JsonNode(n.id, EPANET_NODE_TYPES[n.node_type])
        data_dict["nodes"].append(json_node)

    links = network.links.store
    for l in links.values():
        json_link = JsonLink(l.start.id, l.end.id)
        link_type = EPANET_LINK_TYPES[l.link_type]
        if link_type == "Pipe":
            pass # add extra node
        data_dict["links"].append(json_link)
        print(l)