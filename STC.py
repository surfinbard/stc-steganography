import numpy as np
from treelib import Node, Tree

# currstate muda a cada pulo
    
# todo: check how H dimensions should be defined
# todo: remove camelCase
# todo: remove all unneccessary global vars

# trellis will be a graph made of nodes, like so:
class node:
    def __init__(self, state, value, y_bit):
        self.state = state
        self.value = value
        self.y_bit = y_bit
        self.prev_1 = None
        self.prev_2 = None
        self.next_1 = None
        self.next_2 = None

y = []
h = []
sub_h = []
cover = []
message = []
curr_state = 0

# i refers to current message index 
i = 0
# col refers to indexes of current cover, y, H and trellis columns 
col = 0

# empty trellis
def generate_trellis(sub_width, sub_height):
    for item in range(len(message)):
        get_block(sub_width, sub_height)

def get_block(sub_width, sub_height):
    block = []

    # adding h^2 rows to block 
    for item in range(sub_height ** 2):
        block.append([])
    
    # adding w+1 columns to block, with nodes containing only state values
    for row in range(len(block)):
        for column in range(sub_width + 1):
            block[row][column] = node(row, None, None, None, None, None, None)

    return block   

def generate_h(sub_h):
    sub_height = len(sub_h)
    sub_width = len(sub_h[0])

    # H size hardcoded until further notice
    h_width = 8
    h_height = 4

    for row in range(h_height):
        h.append([])
        for column in range(h_width):

            # row 0 col 0, row 1 col 2, row 2 col 4, row 3 col 6...  
            if (row == column / sub_width):
            
                # placing sub_h inside h, item by item
                for y in range(sub_height):
                    for x in range(sub_width):
                        h[row + x][column + y] = sub_h[x][y]
    return h

def generate_sub_h():
    sub_width = integer_input("Submatrix width: ")
    sub_height = integer_input("Submatrix height: ")

    print("We're now building the submatrix, element by element.\n")

    for row in range(sub_height):
        for column in range(sub_width):
            sub_h[row][column] = binary_input("Enter binary number for row %, column %: " % (row, column))

    print("Submatrix done!\n")
    print("Generating submatrix...\n")
    print(sub_h)

# todo
# repeating same movement process until no more message bits exist
# rinse repeat (goto in)
# return optimal y at end
def embed():

    pass

def move_inside_block(sub_width):
    for column in range(sub_width):
        for row in range(len(trellis)):
            curr_node = trellis[row][col]
            if (curr_node.value != None):
                add_edge(curr_node, 'without_h')
                add_edge(curr_node, 'with_h')
        col += 1

# paths apppendado a cada fim de bloco, pos remocao de orfaos
def end_of_block():
    for row in range(len(trellis)):
        lsb = get_lsb(trellis[row][col].state)
        if lsb != message[i]:
            trellis[row][col].value = None

def move_between_blocks():
    i += 1
    for row in range(len(trellis)):
        curr_node = trellis[row][col]
        if (curr_node.value != None):
            add_edge(curr_node, 'between_blocks')


# todo
# !next i?
# last column: add zeroes to bottom if #rows < sub_height
def end_of_trellis():
    pass

def find_optimal_y(last_column):
    costs = []
    for item in last_column:
        if item.value:
            costs.append(item.value)
    min_cost = min(costs)
    # todo: update this for btree
    return next(item for item in paths if item[-1]["value"] == min_cost)

def extract():
    return np.matmul(h, y)

def get_h_column():
    column = []
    for row in h:
        column.append(h[row][col])
    return column

def add_edge(curr_node, mode):
    match mode:
        case 'without_h':
            value = curr_node.value if cover[col] == 0 else curr_node.value + 1
            # passing state, value (weight) and y bit
            new_node = node(curr_node.state, value, 0)
            curr_node.next_1 = new_node
            new_node.prev_1 = curr_node
            # todo: figure out how to access nodes by keys. memaddresses?
            paths.create_node(new_node, "jane", parent="harry")
        case 'with_h':
            state = curr_node.state ^ get_h_column()
            value = curr_node.value if cover[col] == 1 else curr_node.value + 1
            # passing state, value (weight) and y bit
            new_node = node(state, value, 1)
            curr_node.next_2 = new_node
            new_node.prev_2 = curr_node    
        case 'between_blocks':
            # for future reference: next state = bin(curr_state) - 1 casteado p int
            state = 0 if (curr_node.state == (0 or 1)) else 1
            # y bit = None (no y reading in block transition)
            new_node = node(state, curr_node.value)
            if curr_node.state == 0:
                curr_node.next_1 = new_node
                new_node.prev_1 = curr_node
            else:
                curr_node.next_2 = new_node
                new_node.prev_2 = curr_node    

# todo
def calc_weight():
    pass

def get_lsb(value):
    return value % 2

def img_to_lsb():
    # hardcoded until conversion function available
    return [1, 0, 1, 1, 0, 0, 0, 1]

def integer_input(output):
    while True:
        value = input(output)
        if (not value.strip().isdigit()):
                print("Integers only, please.\n")
        else:
            break
    return value

def binary_input(output):
    while True:
        value = input(output)
        if (int(value.strip()) != (0 or 1)):
                print("Base 2 only, please.\n")
        else:
            break
    return value

if __name__ == '__main__':
#     
#    print("\nHello! Welcome to our approach to PLS embedding using Syndrome-Trellis Coding.\n")
#    print("We hope this command-line finds you well.\n\n")
#
##    print("For now, we'll leave the creation of the submatrix to you, user.\n")
##    sub_h = generate_sub_h()
#    print("Until further coding, submatrix is fixed at [[1, 0], [1, 1]].")
#    sub_h = [[1, 0], [1, 1]]
#    trellis = generate_trellis(2, 2)
#
#    print("Generating matrix H...\n")
#    h = generate_h(sub_h)
#    print("H = %\n" % h)
#
#    cover = img_to_lsb()
#    print("Cover x has been previously selected from directory containing this program, then converted into LSB vector.")
#    print("Cover: %" % cover)
#
#    print("For now, we'll have a fixed message vector [0, 1, 1, 1].")
#    message = [0, 1, 1, 1]
#
#    y = embed()
#    print("Found optimal y.")
#    print("y = %" % y)

    print("\nHe-hewwo user ><")
    print("Let's test some functions!")
    print("u ready?\n")
    print(">be me\n")

    root_node = node(0, 0, y[0])
    paths = Tree()
    paths.create_node(root_node, 'root')