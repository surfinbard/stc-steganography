import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from ete3 import Tree

def select_img():
    while True:
        cover_number = strict_integer_input("\nSelect image as cover [1-10]:")
        if (cover_number > 10):
            print("\nUp to 10 only!")
        else:
            break
    path = './' + str(cover_number) + '.pgm'
    img_to_lsb(path)

def img_to_lsb(path):
    img = Image.open(path).convert('L')
    pixel_vector = np.asarray(img).flatten()

    for i in range(len(pixel_vector)):
        pixel_vector[i] %= 2
    return pixel_vector
    
def get_lsb(value):
    return value % 2

# maybe if this returns a string it can be used for the trellis fix. check
def get_states(sub_height):
    states = []
    for i in range(2 ** sub_height):
        b = format(i, 'b')
        b = str(0) * (sub_height - len(b)) + b
        states.append(b)
    return states

def get_h(sub_h, payload_size, message_size):

    sub_height = len(sub_h)
    sub_width = len(sub_h[0])
    h_width = message_size
    h_height = payload_size
    h = np.zeros((h_height, h_width), dtype=int)

    def place_submatrix(h_row, h_column):
        for row in range(sub_height):
            for column in range(sub_width):
                if (h_row + row < h_height):
                    h[h_row + row][h_column + column] = sub_h[row][column]

    for row in range(h_height):
        for column in range(h_width):
            if (column == row * sub_width):
                place_submatrix(row, column)

    return h  

def get_column(h, col, sub_width, sub_height):
    column = ''
    offset = int(col/sub_width)
    for row in range(offset, offset + sub_height):
        if (row == len(h)):
            break
        column = column + str(h[row][col])
    return column[::-1]

def add_edge(tree, node, cover_index, y_bit):
    cost = cover[cover_index - 1] ^ y_bit
    weight = node.weight + cost

    match y_bit:
        case 0:
            next_state = node.state
        case 1:
            column = get_column(h, cover_index - 1, sub_width, sub_height)
            # cut submatrix adjustment
            while (len(column) < sub_height):
                column = '0' + column
            next_state = int(node.state) ^ int(column)

    existing_node = tree.search_nodes(state=next_state, level=cover_index)
    
    if (existing_node):
        if (existing_node[0].weight > weight):
            node.add_child(existing_node)
            existing_node.add_features(dist=cost, weight=weight, y_bit=y_bit)
    else:
        node.add_child(name='s' + str(next_state) + 'c' + str(cover_index), dist=cost)
        node.add_features(weight=weight, y_bit=y_bit, state=next_state, level=cover_index)

def connect_blocks(node):
    next_state = '0' + node.state[:-1]
    existing_node = tree.search_nodes(state=next_state)

    if (existing_node):
        if (existing_node.weight > node.weight):
            node.add_child(existing_node)
            existing_node.add_feature(weight=node.weight)
    else:
            node.add_child(dist=0, name='s' + next_state + 'p' + str(message_index+1))
            node.add_features(state=next_state, level='p'+str(message_index+1), weight=node.weight, y_bit=None) 

def move_between_blocks(message_index, cover_index):
    column_nodes = tree.search_nodes(level=cover_index)
    for node in column_nodes:
        if node.state[-1] == message_index:
            connect_blocks(node)

def move_inside_block(message_index, cover_index, sub_width, tree):
    for i in range(sub_width):
        column_nodes = tree.search_nodes(level=cover_index)
        cover_index += 1
        for node in column_nodes:
            add_edge(tree, node, cover_index, 0)
            add_edge(tree, node, cover_index, 1)
    move_between_blocks(message_index, cover_index)

def embed(message_index):
    while (len(message) > message_index):
        move_inside_block(message_index, cover_index, sub_width, tree)
        message_index += 1

def get_y(node):
    y = []
    while node:
        y.insert(0, node.y_bit)
        node = node.up
    return y

def get_states():
    states = []
    for i in range(2 ** sub_height):
        b = format(i, 'b')
        b = str(0) * (sub_height - len(b)) + b
        states.append(b)
    return states

def init_trellis():
    tree = Tree()
    root = tree.add_child(name='s' + states[0] + 'p0')
    root.add_features(dist=0, weight=0, state=states[0], level=0)
    return tree

def strict_integer_input(output):
    while True:
        value = input(output + ' ')
        if (not value.strip().isdigit()):
                print("\nIntegers only, please.\n")
        else:
            break
    return int(value)

def strict_binary_input(output):
    while True:
        value = input(output + ' ').strip()
        non_binary = None
        for character in value:
            if (not (character == '0' or character == '1')):
                non_binary = True
                break
        if (non_binary or len(value) == 0):
            print("\nBase 2 numbers only, please.\n")
        else:
            break
    return int(value)

def get_sub_h():
    sub_h = []
    sub_width = strict_integer_input("\nSubmatrix width: ")
    sub_height = strict_integer_input("Submatrix height: ")

    print("We're now building the submatrix, element by element.\n")

    for row in range(sub_height):
        sub_h.append([])
        for column in range(sub_width):
            sub_h[row].append(strict_binary_input(f'Enter binary number for row {row}, column {column}: '))

    print("Inputs done!\n")
    print("Generating submatrix...\n")
    print(sub_h)
    return sub_h

def generate_graph(title, x, y, x_label, y_label):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def optimize_syndrome():
    pass

if __name__ == '__main__':
    message = [0,1,1,1]
    message_index = 0
    cover = [1,0,1,1,0,0,0,1]
    cover_index = 0
    sub_h = [[1,0],[1,1]]
    sub_height = 2
    sub_width = 2
    h = get_h(sub_h, 4, 8)
    states = get_states()
    tree = init_trellis()

    embed(message_index)