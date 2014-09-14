# File input and output library for
# reading and writing graph data  

import pickle
import networkx as nx

def read_graph(filename):
    ''' Read graph from file, raise IOError if cannot do it '''
    graph = None

    if filename.endswith('.yaml'):
        try:
            import yaml
        except ImportError as e:
            print('E: cannot read graph from file in YAML format.')
            print('Please install PyYAML or other similar package '\
                  'to use this functionality.')
            raise IOError
        else:
            print('Read graph from {0} in YAML format'.format(filename))
            graph = nx.read_yaml(filename)
    else:
        print('Read graph from {0} in pickle format'.format(filename))
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
    return graph

def write_graph(graph, filename):
    ''' Write graph to file, raise IOError if cannot do it '''
    if filename.endswith('.yaml'):
        try:
            import yaml
        except ImportError as e:
            print('E: cannot write graph to file in YAML format.')
            print('Please install PyYAML or other similar package '\
                  'to use this functionality.')
            raise IOError
        else:
            print("Write constructed graph to: {0} "\
                  "in YAML format".format(filename))
            nx.write_yaml(graph, filename)
    else:
        print("Write constructed graph to: {0} "\
              "in pickle format".format(filename))
        with open(filename, 'wb') as f:
            pickle.dump(graph, f, protocol=pickle.HIGHEST_PROTOCOL)
