from epanettools.epanettools import EPANetSimulation
import json

EPANET_NODE_TYPES = {0: 'Junction', 1: 'Reservoir', 2: 'Tank'}
EPANET_LINK_TYPES = {0: 'CVPipe', 1: 'Pipe',  2: 'Pump', 3: 'PRV', 4: 'PSV', 5: 'PBV', 6: 'FCV', 7: 'TCV', 8: 'GPV'}


class JsonNode(dict):
    def __init__(self, id_, type_):
        super().__init__()
        self.__setitem__("id", id_)
        self.__setitem__("type", type_)


class JsonLink(dict):
    def __init__(self, source, target):
        super().__init__()
        self.__setitem__("source", source)
        self.__setitem__("target", target)


def write_json_file(graph_dict):
    with open("static/network_test.json", 'w') as json_file:
        json_file.write(json.dumps(graph_dict))


def get_network_nodes(network_):
    nodes = network_.nodes.store
    json_nodes_ = []
    for n in nodes.values():
        jsn_n = JsonNode(n.id, EPANET_NODE_TYPES[n.node_type])
        json_nodes_.append(jsn_n)
    return json_nodes_


def get_network_links(network_):
    links = network_.links.store
    json_links_ = []
    json_nodes_ = []
    for l in links.values():
        link_type = EPANET_LINK_TYPES[l.link_type]
        if link_type in ("Pump", "PSV", 'CVPipe'):
            json_nodes_.append(JsonNode(l.id, link_type))
            json_links_.append(JsonLink(l.start.id, l.id))
            json_links_.append(JsonLink(l.id, l.end.id))
        else:
            jsn_l = JsonLink(l.start.id, l.end.id)
            json_links_.append(jsn_l)
    return json_links_, json_nodes_


if __name__ == '__main__':
    network = EPANetSimulation('network_test.inp').network

    json_nodes = get_network_nodes(network)
    json_links, extra_links = get_network_links(network)
    json_nodes.extend(extra_links)
    data_dict = {"nodes": json_nodes,
                 "links": json_links}

    write_json_file(data_dict)