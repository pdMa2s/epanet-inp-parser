import json
import wntr


class JsonNode(dict):
    def __init__(self, id_, type_, x, y):
        super().__init__()
        self.__setitem__("id", id_)
        self.__setitem__("type", type_)
        self.__setitem__("x", x)
        self.__setitem__("y", y)


class JsonLink(dict):
    def __init__(self, source, target):
        super().__init__()
        self.__setitem__("source", source)
        self.__setitem__("target", target)


class JsonNetwork:
    def __init__(self, nodes=None, links=None):
        self.nodes = nodes if nodes is not None else []
        self.links = links if links is not None else []
        self.dimensions = (None, None)

    def add_node(self, n_id, n_type, n_x, n_y):
        self.nodes.append(JsonNode(n_id, n_type, n_x, n_y))

    def add_links(self, l_source, l_target):
        self.links.append(JsonLink(l_source, l_target))

    def set_network_nodes(self, network_):
        node_registry = network_.nodes()
        for node_id, node in node_registry:
            x, y = node.coordinates
            jsn_n = JsonNode(node_id, node.node_type, x, y)
            self.nodes.append(jsn_n)

    def set_network_links(self, network_):
        link_registry = network_.links()
        for link_id, link in link_registry:
            start_node = link.start_node
            end_node = link.end_node
            if link.link_type in ("Pump", "Valve"):
                start_coordinates = start_node.coordinates
                end_coordinates = end_node.coordinates
                self.nodes.append(
                    JsonNode(link_id, link.link_type, *get_midway_point(start_coordinates, end_coordinates)))
                self.links.append(JsonLink(start_node.name, link_id))
                self.links.append(JsonLink(link_id, end_node.name))
            else:
                jsn_l = JsonLink(start_node.name, end_node.name)
                self.links.append(jsn_l)

    def build_network(self, wntr_network):
        self.set_network_nodes(wntr_network)
        self.set_network_links(wntr_network)

    def get_dimensions(self):
        min_x, max_x, min_y, max_y = 10**6, -10**6, 10**6, -10**6
        for n in self.nodes:
            if n['x'] < min_x:
                min_x = n['x']
            if n['x'] > max_x:
                max_x = n['x']
            if n['y'] < min_y:
                min_y = n['y']
            if n['y'] > max_y:
                max_y = n['y']
        return min_x, max_x, min_y, max_y


def write_json_file(graph_dict):
    with open("static/network_test.json", 'w') as json_file:
        json_file.write(json.dumps(graph_dict))


def get_midway_point(coords_1, coords_2):
    return coords_1[0] - coords_2[0], coords_1[1] - coords_2[1]


def translate_coordinates_from_epanet_to_web_standard(nodes, x_dims, y_dims, scale):
    min_x, min_y = abs(x_dims[0]), abs(y_dims[1])
    max_y = y_dims[1] + min_y
    max_x = x_dims[1] + min_x
    for n in nodes:
        n['x'] += min_x
        n['y'] += min_y
        n['y'] = max_y - n['y']
        n['x'] = n['x'] * scale[0] / max_x
        n['y'] = n['y'] * scale[1] / max_y


if __name__ == '__main__':
    network = wntr.network.WaterNetworkModel('network_test.inp')

    json_network = JsonNetwork()
    json_network.build_network(network)
    network_min_x, network_max_x, network_min_y, network_max_y = json_network.get_dimensions()
    translate_coordinates_from_epanet_to_web_standard(json_network.nodes, (network_min_x, network_max_x),
                                                      (network_min_y, network_max_y), (1200, 800))
    data_dict = {"nodes": json_network.nodes,
                 "links": json_network.links}

    write_json_file(data_dict)
    print("Done! Inp file parsed")