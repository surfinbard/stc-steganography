import math
import random
import numpy as np
import matplotlib.pyplot as plt
from bitstring import BitArray
from PIL import Image
from ete3 import Tree

cover_index = 0
message_index = 0
y = []
cover = []
path = ''
stego_img = None

def get_user_input():

    while True:
        option = input("Would you like to choose a message to hide (1) \nor to generate random messages and see a graphical representations of their embedding efficiencies (2)? ")
        if (not (option == '1' or option == '2')):
            print("Unrecognized input. Try again.")
        else:
            return option

def get_user_message(sub_width):

    def txt_to_bin(str):
        txt_bits = []
        dico = {}
        for i in range(256):
            dico[chr(i)] = i
        w = ""
        for c in str:
            p = w + c
            if(dico.get(p) != None):
                w = p
            else:
                dico[p] = len(dico)
                txt_bits.append(dico[w])
                w = c
        txt_bits.append(dico[w])
        message = np.empty(len(txt_bits) * 12, 'uint8')
        for i in range(len(txt_bits)):
            str_bits = format(txt_bits[i], '012b')
            for j in range(len(str_bits)):
                message[i * 12 + j] = str_bits[j]
        return message

    while True:
        txt_input = input("What would you like to hide today? ")
        bin_input = txt_to_bin(txt_input)
        if len(bin_input) > len(cover):
            print("\nThis message is too large for the selected cover! Try something shorter.")
        else:
            #size = len(cover)//sub_width
            #str(bin_input).ljust(size - len(bin_input), '0')
            return bin_input

def get_random_payloads(message_number, message_length):
    return np.random.randint(0, 2, (message_number, message_length))

def strict_integer_input(output):
    while True:
        value = input(output + ' ')
        if (not value.strip().isdigit()):
                print("\nIntegers only, please.")
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
    global path
    while True:
        cover_number = strict_integer_input("\nSelect image as cover [1-12]:")
        if (cover_number > 12):
            print("\nUp to 12 only!")
        else:
            break
    path = './img/' + str(cover_number) + '.pgm'
    img_bits = img_to_lsb(path)
    print("Cover: " + str(img_bits) + '\n')
    return img_bits

def img_to_lsb(path):
    img = Image.open(path).convert('L')
    return  np.mod(np.asarray(img), 2).flatten()

def get_optimal_sub_h(edge_size, alpha, sub_height, sub_width, iteration_number, message_number, path = ()):
    if(path):
        image = open_image(path)
    else:
        image = generate_random_img()
    pixels = get_pixels(image)
    x = pixels_to_LSB(pixels)
    message_length = len(pixels) * alpha
    messages = get_random_msg(message_length, message_number)
    submatrixes = np.empty((iteration_number, sub_height, sub_width), "uint8")
    avg_efficiencies = np.empty(iteration_number)
    for i in range(iteration_number):
        sub_h = get_random_sub_h(sub_height, sub_width)
        submatrixes[i] = sub_h
        H = createH(sub_h)
        avg_efficiencies[i] = get_avg_efficiency(x, H, sub_h, messages, edge_size)
    return submatrixes[np.argmax(avg_efficiencies)]

def get_random_sub_h(sub_height, sub_width):
    sub_h = np.random.randint(0, 2, (sub_height, sub_width), "uint8")
    if(not np.isin(1, sub_h[0])):
        sub_h[0][np.random.randint(sub_width)] = 1
    if(not np.isin(1, sub_h[sub_height - 1])):
        sub_h[sub_height - 1][np.random.randint(sub_width)] = 1
    return sub_h

def get_efficiency(message_length, distortion):
    if(distortion == 0):
        return message_length / 0.1
    return message_length / distortion

def get_avg_efficiency(x, H, sub_h, messages, edge_size):
    message_number = len(messages)
    efficiencies = np.zeros(message_number)
    for i in range(message_number):
        message = messages[i]
        y = ugly_trellis(H, sub_h, x, message)
        distortion = get_distortion(x, y)
        efficiencies[i] = get_efficiency(len(message), distortion)
    avg_efficiency = np.mean(efficiencies)
    return avg_efficiency

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
    h = np.zeros((h_height, h_width), dtype='int8')

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

    for i in range(len(y), len(cover)):
        y.append(cover[i])

    print("\nCalculating stego object done.")
    if(show_img):
        print("Opening both images...")
    display_imgs()

def display_imgs():
    global stego_img

    img = Image.open(path).convert('L')
    img_pixels = np.asarray(img, 'uint8')

    def get_stego_pixels():
        global path, cover
        stego_pixels = []
        difference = []
        difference = np.absolute(y - cover)
        difference_matrix = vector_to_matrix(difference)

        for i in range(len(img_pixels)):
            stego_pixels.append([])
            for j in range(len(img_pixels[0])):
                stego_pixels[i].append(img_pixels[i][j] + difference_matrix[i][j])
                # Instead of adding 1, we retrive 1 because 255 is the maximum
                if(stego_pixels[i][j] == 256):
                    stego_pixels[i][j] = 254
        return np.asarray(stego_pixels, 'uint8')

    def vector_to_matrix(vector):
        matrix = []
        cover_rows = len(img_pixels)
        cover_columns = len(img_pixels[0])
        for i in range(cover_rows):
            matrix.append([])
            for j in range(cover_columns):
                matrix[i].append(vector[i * cover_rows + j])
        return matrix

    cover_img = Image.fromarray(img_pixels, 'L')
    if(show_img):
        cover_img.show(title="Cover image")
    stego_pixels = get_stego_pixels()
    stego_img = Image.fromarray(stego_pixels, 'L')
    if(show_img):
        stego_img.show(title="Stego image")

def extract(h):

    def bin_to_txt(message):
        str = ""
        dico = {}
        for i in range(256):
            dico[i] = chr(i)
        txt_bits = packed(message)
        v = txt_bits[0]
        w = dico[v]
        str += w
        for i in range(1, len(txt_bits)):
            v = txt_bits[i]
            if(dico.get(v) != None):
                entry = dico[v]
            else:
                entry = w + w[0]
            str += entry
            dico[len(dico)] = w + entry[0]
            w = entry
        return str

    def packed(message):
        txt_bits = []
        for i in range(0, len(message), 12):
            txt_bits.append(int(''.join(np.array(message, '<U1')[i:i+12]), 2))
        return txt_bits

    m = np.matmul(h, np.mod(np.asarray(stego_img),2).flatten())
    for i in range(len(m)):
        m[i] %= 2

    txt_output = bin_to_txt(list(m))

    print("\nMessage retrieved.")
    print("M = " + txt_output + '\n')

def generate_graph(title, x, y, x_label, y_label):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def calculate_distortion(cover_img, stego_img):
    return np.absolute(np.asarray(cover_img).flatten() - np.asarray(stego_img).flatten()).sum()

def init_global_variables():
    global cover_index, message_index, y, tree, stego_img
    cover_index = 0
    message_index = 0
    y = []
    tree = init_trellis()
    stego_img = []

if __name__ == '__main__':

    print("\nHello! Welcome to our approach to PLS embedding using Syndrome-Trellis Coding.")
    print("We hope this command-line finds you well.\n")


    sub_h = [[1, 0], [1, 1]]
    sub_h = get_random_sub_h(4, 7)
    print("Submatrix currently fixed at\n", np.asarray(sub_h))
    sub_height = len(sub_h)
    sub_width = len(sub_h[0])
    tree = init_trellis()

    cover = select_img()
    option = get_user_input()
    show_img = True

    match(option):
        case '1':
            message = get_user_message(sub_width)
            print("Generating matrix H...\n")
            h = get_h(sub_h, len(message), len(cover))
            print("H = \n" + str(h))

            embed()
            extract(h)

            distortion = calculate_distortion(Image.open(path).convert('L'), stego_img)
            print("With a distortion of :", distortion)
            print("For a message of length :", len(message))
            print("Which give an efficiency of :", get_efficiency(len(message), distortion))
        case '2':
            show_img = False
            message_number = 5
            abscissa = []
            ordinate = []
            for inverse_alpha in range(40, 60 + 2, 2):
                print("1/alpha =", inverse_alpha)
                alpha = 1 / inverse_alpha
                message_length = math.floor(len(cover) * alpha) 
                messages = get_random_payloads(message_number, message_length)
                h = get_h(sub_h, len(messages[0]), len(cover))
                efficiencies = []
                for i in range(message_number):
                    print("    message", i, "/", message_number)
                    message = messages[i]
                    init_global_variables()
                    
                    embed()
                    distortion = calculate_distortion(Image.open(path).convert('L'), stego_img)
                    efficiencies.append(get_efficiency(message_length, distortion))
                abscissa.append(inverse_alpha)
                ordinate.append(np.asarray(efficiencies).mean())
            generate_graph("For n = " + str(len(cover)) + " sub_width = " + str(sub_width) + " sub_height = " + str(sub_height), abscissa, ordinate, "1/alpha", "efficiency")
