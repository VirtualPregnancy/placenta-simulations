import numpy as np

#routines used for testing of 'functional models'

def is_float(str):
    try:
        num = float(str)
    except ValueError:
        return False
    return True

def read_exnode(filename):
    # count nodes for check of correct number for the user, plus use in future arrays
    count_node = 0
    # Initialise array of node numbers and values
    node_array = np.empty((0, 10)) #assumes a maximum of ten fields
    # open file
    with open(filename) as f:
        # loop through lines of file
        while 1:
            line = f.readline()
            if not line:
                break  # exit if done with all lines
            # identifying whether there is a node defined here
            line_type = str.split(line)[0]
            if (line_type == 'Node:'):  # line defines new node
                count_node = count_node + 1  # count the node
                count_atribute = 0  # intitalise attributes of the node (coordinates, radius)
                node_array = np.append(node_array, np.zeros((1, 10)),
                                       axis=0)  # initialise a list of attributes for each node
                node_array[count_node - 1][count_atribute] = int(str.split(line)[1]) - 1
            else:
                line_num = is_float(line_type)  # checking if the line is a number
                if (line_num):  # it is a number
                    if not "index" in line:
                        count_atribute = count_atribute + 1
                        node_array[count_node - 1][count_atribute] = float(str.split(line)[0])

    if (count_atribute < 10):
        node_array = np.delete(node_array, np.s_[count_atribute + 1:10], axis=1)
    total_nodes = count_node
    return  node_array

def read_txt(filename):
    count_length = 0
    data_array = np.empty((0,10)) #assumes a maximum of ten fields

    with open(filename) as f:
        # loop through lines of file
        while 1:
            line = f.readline()
            if not line:
                break  # exit if done with all lines
            line_type = str.split(line)[0]
            line_num = is_float(line_type)  # checking if the line is a number
            if (line_num):  # it is a number
                data_array = np.append(data_array, np.zeros((1, 10)),
                                       axis=0)  # initialise a list of attributes for each node
                data_size = len(str.split(line))-1
                for i in range(0,len(str.split(line))):
                    data_array[count_length,i] = str.split(line)[i]
                count_length = count_length + 1

    if (data_size < 10):
        data_array = np.delete(data_array, np.s_[data_size + 1:10], axis=1)

    return data_array

def compare_perfusion_clark2015():

    #read in the terminal .exnode file
    nodes_output = read_exnode('../fetoplacental/interface2015/output/terminal.exnode')
    nodes_expected = read_exnode('../fetoplacental/interface2015/expected-results/terminal.exnode')
    check_true = np.isclose(nodes_output[:,:],nodes_expected[:,:]).all()
    return check_true

def compare_perfusion_byrne2020():

    #read in the terminal .exnode file
    nodes_output = read_exnode('../fetoplacental/two_umb_arteries/output/terminal.exnode')
    nodes_expected = read_exnode('../fetoplacental/two_umb_arteries/expected-results-no-anast/terminal.exnode')
    check_true = np.isclose(nodes_output[:,:],nodes_expected[:,:]).all()
    return check_true

def compare_ellipsoid_tree_grow():

    #read in the terminal .exnode file
    nodes_output = read_exnode('../geometry/grow-tree-ellipsoid/output/terminals.exdata')
    nodes_expected = read_exnode('../geometry/grow-tree-ellipsoid/expected-results/terminals.exdata')
    check_true = np.isclose(nodes_output[:,:],nodes_expected[:,:]).all()
    return check_true

def compare_cuboid_tree_grow():

    #read in the terminal .exnode file
    nodes_output = read_exnode('../geometry/grow-tree-cuboid/output/terminals.exdata')
    nodes_expected = read_exnode('../geometry/grow-tree-cuboid/expected-results/terminals.exdata')
    check_true = np.isclose(nodes_output[:,:],nodes_expected[:,:]).all()
    return check_true