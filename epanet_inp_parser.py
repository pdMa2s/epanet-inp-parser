import json
from epanet import epamodule

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


def get_network_nodes():
    node_count = epamodule.ENgetcount(epamodule.EN_NODECOUNT)
    json_nodes_ = []
    for n_idx in range(1, node_count+1):
        node_id = epamodule.ENgetnodeid(n_idx)
        node_type = epamodule.ENgetnodetype(n_idx)
        jsn_n = JsonNode(node_id.decode("utf-8"), EPANET_NODE_TYPES[node_type])
        json_nodes_.append(jsn_n)
    return json_nodes_


def get_network_links():
    link_count = epamodule.ENgetcount(epamodule.EN_LINKCOUNT)
    json_links_ = []
    json_nodes_ = []
    for l_idx in range(1, link_count+1):
        link_type = epamodule.ENgetlinktype(l_idx)
        link_type = EPANET_LINK_TYPES[link_type]
        link_id = epamodule.ENgetlinkid(l_idx).decode("utf-8")
        link_start_idx, link_end_idx = epamodule.ENgetlinknodes(l_idx)
        start_node_id = epamodule.ENgetnodeid(link_start_idx).decode("utf-8")
        end_node_id = epamodule.ENgetnodeid(link_end_idx).decode("utf-8")
        if link_type in ("Pump", "PSV", 'CVPipe'):

            json_nodes_.append(JsonNode(link_id, link_type))
            json_links_.append(JsonLink(start_node_id, link_id))
            json_links_.append(JsonLink(link_id, end_node_id))
        else:
            jsn_l = JsonLink(start_node_id, end_node_id)
            json_links_.append(jsn_l)
    return json_links_, json_nodes_


if __name__ == '__main__':
    epamodule.ENopen('network_test.inp', "/dev/null")

    json_nodes = get_network_nodes()
    json_links, extra_links = get_network_links()
    json_nodes.extend(extra_links)
    data_dict = {"nodes": json_nodes,
                 "links": json_links}

    write_json_file(data_dict)
    print("Done! Inp file parsed")