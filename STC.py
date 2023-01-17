import numpy as np
import array as arr
import numpy as np

# global vars
class node:
    def __init__(self, state = None, weight = None, y_bit = None, prev_1 = None, prev_2 = None, next_1 = None, next_2 = None):
        self.state = state
        self.weight = weight
        self.y_bit = y_bit
        self.prev_1 = prev_1
        self.prev_2 = prev_2
        self.next_1 = next_1
        self.next_2 = next_2

# i refers to current message index 
i = 0
# col refers to indexes of current y, H and trellis columns 
col = 0

y = []
h = []
sub_h = []
cover = []
message = []
curr_state = 0
curr_node = node(curr_state, 0, None, None, None, None, None)
paths = []

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

# repeating same movement process until no more message bits exist
# rinse repeat (goto in)
def embed():
    # concatena state em respectivo prev state, se existe
    
    # return optimal y at end
    pass

# in: itera coluna i, se tiver nó:
# add edge - (atualiza vars: )
# add edge \/ (atualiza vars: )
# checa duplicidade, se sim, mantém peso menor
# calc peso
def move_inside_block():
    pass

def add_edge():
    pass

def calc_weight():
    pass

# end of block: itera currPaths. se state%2 != mBit, pop
def end_of_block():
    pass

# next i? between; (clear first block, add new block)?

# between: itera col i, se há nó, 0 in, LSB out
# atualiza vars: currState, paths
def move_between_blocks():
    pass

# !next i? rotina de fim
# fim: (se não há mi+1) itera col i, se 2+ nós, seleciona menor weight
# optimal Y já está pronto. só pegar pelo currState no state do nó final do vetor correspondente em paths
def end_of_trellis():
    pass

# todo: make this not look like an ape's code
def find_optimal_y(last_column):
    weights = []
    for item in last_column:
        if item.weight:
            weights.append(item.weight)
    return min(weights)

def extract():
    pass

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
    # user-set sub_h width
    sub_width = integer_input("Submatrix width: ")
    # user-set sub_h height
    sub_height = integer_input("Submatrix height: ")

    print("We're now building the submatrix, element by element.\n")

    # user-set submatrix h
    for row in range(sub_height):
        for column in range(sub_width):
            sub_h[row][column] = binary_input("Enter binary number for row %, column %: ", (row, column))

    print("Submatrix done!\n")
    print("Generating submatrix...\n")
    print(sub_h)

def img_to_lsb():
    # hardcoded until conversion function available
    return [1, 0, 1, 1, 0, 0, 0, 1]

if __name__ == '__main__':
     
    print("Hello! Welcome to our approach to PLS embedding using Syndrome-Trellis Coding.\n")
    print("We hope this command-line finds you well.\n\n")

#    print("For now, we'll leave the creation of the submatrix to you, user.\n")
#    sub_h = generate_sub_h()
    print("Until further coding, submatrix is fixed at [[1, 0], [1, 1]].")
    sub_h = [[1, 0], [1, 1]]
    
    print("Generating matrix H...\n")
    h = generate_h(sub_h)
    print("H = %\n", h)

    cover = img_to_lsb()
    print("Cover x has been previously selected from directory containing this program, then converted into LSB vector.")
    print("Cover: %", cover)

    print("For now, we'll have a fixed message vector [0, 1, 1, 1].")

    y = embed()
    print("Found optimal y.")
    print("y = %", y)

# todo: verificar atualizacoes de vars globais
# todo: check how H dimensions should be defined