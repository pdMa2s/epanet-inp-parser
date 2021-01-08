import json
import wntr


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
    node_registry = network_.nodes()
    json_nodes_ = []
    for node_id, node in node_registry:
        jsn_n = JsonNode(node_id, node.node_type)
        json_nodes_.append(jsn_n)
    return json_nodes_


def get_network_links(network_):
    link_registry = network_.links()
    json_links_ = []
    json_nodes_ = []
    for link_id, link in link_registry:
        start_node_id = link.start_node.name
        end_node_id = link.end_node.name
        if link.link_type in ("Pump", "Valve"):
            json_nodes_.append(JsonNode(link_id, link.link_type))
            json_links_.append(JsonLink(start_node_id, link_id))
            json_links_.append(JsonLink(link_id, end_node_id))
        else:
            jsn_l = JsonLink(start_node_id, end_node_id)
            json_links_.append(jsn_l)
    return json_links_, json_nodes_


if __name__ == '__main__':
    network = wntr.network.WaterNetworkModel('network_test.inp')

    json_nodes = get_network_nodes(network)
    json_links, extra_links = get_network_links(network)
    json_nodes.extend(extra_links)
    data_dict = {"nodes": json_nodes,
                 "links": json_links}

    write_json_file(data_dict)
    print("Done! Inp file parsed")