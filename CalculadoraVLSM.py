"""CALCULATOR VLSM MARÍA

Members:
    - Juan Sebastián Barreto Jimenéz
    - Janet Chen He
    - María José Niño Rodriguez
    - David Santiago Quintana Echavarria

"""
# Imports of the necessary libraries
import numpy as np
import math
from tabulate import tabulate

#   Function: decimal_to_binary() 
#   Purpose: Convert a decimal number to binary
#   Argument:
#       number: Decimal number to convert
#       n_format: Number of bits with default value of '8'
#   Return:
#       Binary number
def decimal_to_binary(number, n_format='8'):
    s_format = '0' + n_format + 'b'
    return format(number,s_format)

#   Function: binary_to_decimal() 
#   Purpose: Convert a binary number to decimal
#   Argument:
#       number: Binary number to convert
#   Return:
#       Decimal number
def binary_to_decimal(number_binary):
    return int(number_binary,2)

#   Function: split_base_address() 
#   Purpose: Separate the address in each octet by ".
#   Argument:
#       base_address: Base network address
#   Return:
#       List with base network address in octets
def split_base_address(base_address):
    return list(map(int, base_address.split(".")))

#   Function: build_mask() 
#   Purpose: Generates the network mask from the entered network prefix
#   Argument:
#       number_ones: Network prefix
#   Return:
#       List with the mask in bits in octets
def build_mask(number_ones):
    mask_list = []
    cant_oct = 0
    ones_c = 255
    zeros_c = 0
    oct_c = number_ones//8
    oct_o = number_ones%8
    for i in range(oct_c): # part ones complete
        mask_list.append(ones_c)
        cant_oct += 1
    str_b = ""
    if oct_o != 0:
        cant_oct += 1
        for j in range(8):  # part ones and zeros
            if j < oct_o:
                str_b += '1'
            else:
                str_b += '0'
        mask_list.append(binary_to_decimal(str_b))
    for i in range(4-cant_oct):  # part zeros complete
        mask_list.append(zeros_c)
    return mask_list

#Función que valida la dirección IP base sea de red

#   Function: validate_red_address() 
#   Purpose: Validate the base IP address is network
#   Argument:
#       list_base_address: List with base network address in octets
#       network_prefix: Network prefix
#   Return:
#       Boolean indicating whether the network is valid or not
def validate_red_address(list_base_address, network_prefix):
    mask = build_mask(network_prefix)
    mask_np = np.array(mask)
    list_base_address_np = np.array(list_base_address)
    list_validate_address = list_base_address_np & mask_np
    comparate = 0
    for i in range(4):
        if list_validate_address[i] == list_base_address_np[i]:
            comparate += 1
    if comparate == 4:
        return True
    else:
        return False

# The base IP address is read
base_address = input("Ingrese la dirección IP base: ")
# Base ip address separated
list_base_address = split_base_address(base_address)

# Validate if the IP address is correct
if len(list_base_address) != 4: 
    print("La dirección no es válida")
    exit()

# Read the network prefix
network_prefix = int(input("Ingrese el prefijo de red: "))

# Validate if the IP address is network
if(not(validate_red_address(list_base_address,network_prefix))):
    print("La dirección no es de red")
    exit()

# The number of networks is read
number_networks = int(input("Ingrese el número de redes: "))

# Variable creation
number_networks_bits = []
sub_hosts = {}
sub_networks = {}
sub_networks_end = []

# The number of hosts is read for each network
for i in range(number_networks):
    number_hosts = int(input("Ingrese el número de hosts de la red %d: " % i))
    sub_hosts[i] = [number_hosts, math.ceil(math.log2(number_hosts +2))]

# Sort the subnets from largest to smallest
sub_hosts = sorted(sub_hosts.items(),key=lambda x: x[1], reverse=True)

# Calculate the number of subnets in each subnet
for i in range(number_networks):
    number_networks_bits.append(32 - sub_hosts[i][1][1] - network_prefix)

# VLSM calculation with user entered parameters
for i  in range(number_networks):
    num_hosts = sub_hosts[i][1][1] #[subred id, num bit sub, mascara]
    bit_sub = 32 - network_prefix - num_hosts
    id_sub = ""
    if i == 0:
        if number_networks_bits[0] < 0:
            print("No es posible realizar más redes con los hosts indicados")
            break
        for j in range(bit_sub):
            id_sub += '0'
        bit_sub_base = bit_sub
    else:
        id_sub_prev, bit_sub_prev, mask_sub_prev  = sub_networks[i-1]
        aux_sum = binary_to_decimal(id_sub_prev)+1
        if bit_sub-bit_sub_prev != 0:
            aux_sum *= (2**(bit_sub-bit_sub_prev))
        comparator_max = math.ceil(math.log2(aux_sum))
        if aux_sum %2 == 0:
            comparator_max += 1 
        if comparator_max > number_networks_bits[i]:
            print("No es posible realizar más redes con los hosts indicados")
            break
        id_sub = decimal_to_binary(aux_sum,str(bit_sub))
    sub_networks[i] = [id_sub, bit_sub, 32 - num_hosts]
    b_list_base_address = []
    index_list = network_prefix//8
    index_oct = network_prefix%8
    if(index_list > 3):
        exit()
    list_red = list_base_address[:]
    flag = False
    for j in range(4):
        b_list_base_address.append(decimal_to_binary(list_red[j]))
        space = 8 - index_oct
        if flag:
            space_two = 8 - bit_sub
            if space_two < 0:
                b_list_base_address[j] =  id_sub[space:space+8]
            else:
                flag = False
                b_list_base_address[j] =  id_sub[space:] + b_list_base_address[j][bit_sub:8]
        if j == index_list:
            if bit_sub > space:
                flag = True
                b_list_base_address[j] = b_list_base_address[j][0:index_oct] + id_sub[0:space] + b_list_base_address[j][index_oct+bit_sub:8]
                bit_sub -= space
            else:
                b_list_base_address[j] = b_list_base_address[j][0:index_oct] + id_sub + b_list_base_address[j][index_oct+bit_sub:8]
        list_red[j] = binary_to_decimal(b_list_base_address[j])
    sub_networks_end.append([i+1, sub_hosts[i][1][0], '.'.join([str(int) for int in list_red])+ '/' + str(32 - num_hosts)])
    if i == 0 and number_networks_bits[0] == 0:
        print("No es posible realizar más redes con los hosts indicados")
        break

# The calculated subnets are printed in a table for the user
print('\n',tabulate(sub_networks_end, headers=["Red", "Hosts", "Dirección de red"]))