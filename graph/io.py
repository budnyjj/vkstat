# File input and output library for
# reading and writing graph data

import pickle

try:
    import networkx as nx
except ImportError:
    print('This script requires NetworkX to be installed.')
    exit(1)

def exclude_complex_attrs(graph):
    """Exclude complex attributes from graph."""
    # make copy of graph to count neighbors per node
    res_graph = graph.copy()

    for node_id, node_data in graph.nodes(data=True):
        for attr in node_data:
            if type(node_data[attr]) in (list, dict):
                del res_graph.node[node_id][attr]
    return res_graph

def read_graph(filename):
    """Read graph from file, raise IOError if cannot do it."""
    graph = None

    if filename.endswith('.yaml'):
        try:
            graph = nx.read_yaml(filename)
        except ImportError:
            print('E: cannot read graph from file in YAML format.')
            print('Please install PyYAML or other similar package '
                  'to use this functionality.')
            raise IOError
        else:
            print('Read graph from {0} in YAML format.'.format(filename))
    elif filename.endswith('.gml'):
        try:
            graph = nx.read_gml(filename)
        except ImportError:
            print('E: cannot read graph from file in GML format.')
            print('Please install GML or other similar package '
                  'to use this functionality.')
            raise IOError
        else:
            print('Read graph from {0} in GML format.'.format(filename))
    elif filename.endswith('.net'):
        graph = nx.read_pajek(filename)
        print('Read graph from {0} in PAJECK format.'.format(filename))
    elif filename.endswith('.gexf'):
        graph = nx.read_gexf(filename)
        print('Read graph from {0} in GEXF format.'.format(filename))
    elif filename.endswith('.graphml'):
        graph = nx.read_graphml(filename)
        print('Read graph from {0} in GraphML format.'.format(filename))
    else:
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        print('Read graph from {0} in pickle format.'.format(filename))
    return graph


def write_graph(graph, filename):
    """Write graph to file, raise IOError if cannot do it."""
    if filename.endswith('.yaml'):
        try:
            nx.write_yaml(graph, filename)
        except ImportError:
            print('E: cannot write graph to file in YAML format.')
            print('Please install PyYAML or other similar package '
                  'to use this functionality.')
            raise IOError
        else:
            print('Write constructed graph to: {0} '
                  'in YAML format.'.format(filename))
    elif filename.endswith('.gml'):
        try:
            nx.write_gml(graph, filename)
        except ImportError:
            print('E: cannot write graph to file in GML format.')
            print('Please install pyparsing package '
                  'to use this functionality.')
            raise IOError
        else:
            print('Write constructed graph to: {0} '
                  'in GML format.'.format(filename))
    elif filename.endswith('.net'):
        nx.write_pajek(graph, filename)
        print('Write constructed graph to: {0} '
              'in PAJEK format.'.format(filename))
    elif filename.endswith('.gexf'):
        graph = exclude_complex_attrs(graph)
        nx.write_gexf(graph, filename)
        print('Write constructed graph to: {0} '
              'in GEXF format.'.format(filename))
    elif filename.endswith('.graphml'):
        graph = exclude_complex_attrs(graph)
        nx.write_graphml(graph, filename)
        print('Write constructed graph to: {0} '
              'in GraphML format.'.format(filename))
    else:
        with open(filename, 'wb') as f:
            pickle.dump(graph, f, protocol=pickle.HIGHEST_PROTOCOL)
        print('Write constructed graph to: {0} '
              'in pickle format.'.format(filename))
