import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from ete3 import Tree

cover_index = 0
message_index = 0
y = []

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

def get_h(sub_h, payload_size, message_size):

    sub_height = len(sub_h)
    sub_width = len(sub_h[0])
    h_width = message_size
    h_height = payload_size
    h = np.zeros((h_height, h_width), dtype=int)

    def place_submatrix(h_row, h_column):
        for row in range(sub_height):
            for column in range(sub_width):
                if (h_row + row < h_height and h_column + column < h_width):
                    h[h_row + row][h_column + column] = sub_h[row][column]

    for row in range(h_height):
        for column in range(h_width):
            if (column == row * sub_width):
                place_submatrix(row, column)

    return h  

def init_trellis():
    tree = Tree()
    root = tree.get_tree_root()
    root.add_features(y_bit='-')
    first_node = tree.add_child(name='s' + ''.zfill(sub_height) + 'p0')
    first_node.add_features(dist=0, weight=0, state=''.zfill(sub_height), level='p0', y_bit='-')
    return tree

def get_column(h, sub_width, sub_height):
    global cover_index
    column = ''
    offset = int(cover_index/sub_width)
    for row in range(offset, offset + sub_height):
        if (row == len(h)):
            break
        column = column + str(h[row][cover_index])
    return column[::-1].zfill(sub_height)

def add_edge(tree, node, y_bit):
    global cover_index
    cost = cover[cover_index] ^ y_bit
    weight = node.weight + cost

    match y_bit:
        case 0:
            next_state = node.state
        case 1:
            column = get_column(h, sub_width, sub_height)
            next_state = str(bin(int(node.state, 2) ^ int(column, 2))[2:]).zfill(sub_height)

    existing_node = tree.search_nodes(state=next_state, level=cover_index+1)
        
    if (len(existing_node)):
        existing_node = existing_node[0]
        if (existing_node.weight > weight):
            existing_node.detach()
            node.add_child(existing_node)
            existing_node.add_features(dist=cost, weight=weight, y_bit=y_bit)
    else:
        new_node = node.add_child(name='s' + str(next_state) + 'c' + str(cover_index+1), dist=cost)
        new_node.add_features(weight=weight, y_bit=y_bit, state=next_state, level=cover_index+1)

def move_inside_block(sub_width, tree):
    global cover_index
    for i in range(sub_width):
        if i == 0:
            level = 'p' + str(message_index)
        else:
            level = cover_index
        column_nodes = tree.search_nodes(level=level)
        for node in column_nodes:
            add_edge(tree, node, 0)
            add_edge(tree, node, 1)
        cover_index += 1
    exit_block()

def exit_block():
    global cover_index, message_index, y
    column_nodes = tree.search_nodes(level=cover_index)

    for node in column_nodes:
        if node.state[-1] == str(message[message_index]):
            connect_blocks(node)

def connect_blocks(node):
    global message_index
    next_state = '0' + node.state[:-1]
    existing_node = tree.search_nodes(state=next_state, level=node.level+1)

    if (len(existing_node)):
        existing_node = existing_node[0]
        if (existing_node.weight > node.weight):
            existing_node.detach()
            node.add_child(existing_node)
            existing_node.add_features(weight=node.weight)
    else:
        new_node = node.add_child(dist=0, name='s' + next_state + 'p' + str(message_index+1))
        new_node.add_features(state=next_state, level='p'+str(message_index+1), weight=node.weight, y_bit='-') 
        
        # check if last block
        if(message_index == len(message) - 1):
            get_y(new_node)

def embed():
    global message_index
    for index in range(len(message)):
        message_index = index
        move_inside_block(sub_width, tree)
        
def get_y(node):
    global y
    while node:
        if (isinstance(node.y_bit, int)):
            y.insert(0, node.y_bit)
        node = node.up
        
    print("\nFound optimal y.")
    print("y = " + str(y))

def extract(h):
    m = np.matmul(h, y)
    for i in range(len(m)):
        m[i] %= 2
    
    print("\nMessage retrieved.")
    print("M = " + str(m) + '\n')

def generate_graph(title, x, y, x_label, y_label):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

if __name__ == '__main__':    
     
    print("\nHello! Welcome to our approach to PLS embedding using Syndrome-Trellis Coding.")
    print("We hope this command-line finds you well.\n")

    print("Submatrix currently fixed at [[1, 0], [1, 1]].")
    sub_h = [[1, 0], [1, 1]]
    sub_height = 2
    sub_width = 2
    tree = init_trellis()

    print("Generating matrix H...\n")
    h = get_h(sub_h, 4, 8)
    print("H = \n" + str(h))

#    cover = img_to_lsb()
    cover = [1,0,1,1,0,0,0,1]
    print("\nCover: " + str(cover))

    print("Current message vector fixed at [0, 1, 1, 1].")
    message = [0, 1, 1, 1]

    embed()
    extract(h)