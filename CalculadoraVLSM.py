import numpy as np
import math

def decimal_to_binary(number, cont=0):
    if(cont==0):
        return format(number,"08b")
    else:
        return format(number,"b")

def binary_to_decimal(number_binary):
    return int(number_binary,2)

def split_base_address(base_address):
    return list(map(int, base_address.split(".")))

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
    if(oct_o != 0):
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

def validate_red_address(list_base_address, network_prefix):
    mask = build_mask(network_prefix)
    mask_np = np.array(mask)
    list_base_address_np = np.array(list_base_address)
    list_validate_address = list_base_address_np & mask_np
    comparate_lists = [item for item in list_base_address if item in list_validate_address]
    return len(comparate_lists) == 4

# se lee dirección IP base
base_address = "200.200.200.0" #input("Ingrese la dirección IP base: ")
list_base_address = split_base_address(base_address)
print(list_base_address)
# se lee el prefijo de red
network_prefix = 23 #int(input("Ingrese el prefijo de red: "))
# se lee el numero de redes
number_networks = 3 #int(input("Ingrese el número de redes: "))
number_networks_bits = []
#for i in range(3):
    #number_networks_bits.append(math.ceil(math.log2(number_networks)))

print(number_networks_bits)

# validate red base address
if(not(validate_red_address(list_base_address,network_prefix))):
    print("La dirección no es de red, vuelva a intentar")
    exit()

sub_hosts = {}

#for i in range(number_networks):
#    number_hosts = int(input("Ingrese el número de hosts de la red %d: " % i))
#    sub_hosts[i] = [number_hosts, math.ceil(math.log2(number_hosts +2))]
sub_hosts[0] = [200,8]
sub_hosts[1] = [120,7]
sub_hosts[2] = [80,7]
sub_hosts = sorted(sub_hosts.items(),key=lambda x: x[1], reverse=True)

possible = True
# for i in range(number_networks):   
#     print("TEST",sub_hosts[i][1][1] + number_networks_bits + network_prefix)
#     print("TEST",sub_hosts[i][1][1],number_networks_bits,network_prefix)
#     if( (sub_hosts[i][1][1] + number_networks_bits + network_prefix) > 32):
#         possible=False
#         print("No es posible generar su redes")

sub_networks = {}
sub_networks_end = {}


#### TEST ###
possible = True

if(possible == True):
    for i  in range(number_networks):
        ##################[subred id, num bit sub, mascara]
        num_hosts = sub_hosts[i][1][1]
        bit_sub = 32 - network_prefix - num_hosts
        id_sub = ""
        if i == 0:
            for j in range(bit_sub):
                id_sub += '0'
        else:
            id_sub_prev, bit_sub_prev, mask_sub_prev  = sub_networks[i-1]
            aux_sum = binary_to_decimal(id_sub_prev)+1
            # if(aux_sum > bit_sub_prev):
            #     print("No es posible realizar más redes con los hosts indicados")
            #     exit()
            id_sub = decimal_to_binary(aux_sum,1)
            if bit_sub_prev != bit_sub:
                for j in range(bit_sub - bit_sub_prev):
                    id_sub += '0'
        sub_networks[i] = [id_sub, bit_sub, 32 - num_hosts]
        b_list_base_address = []
        index_list = network_prefix//8
        index_oct = network_prefix%8
        if(index_list > 3):
            exit()
        list_red = list_base_address[:]
        b_list_base_address.append(decimal_to_binary(list_red[index_list]))
        b_list_base_address[0] = b_list_base_address[0][0:index_oct] + id_sub + b_list_base_address[0][index_oct+bit_sub:8]
        list_red[index_list] = binary_to_decimal(b_list_base_address[0])
        sub_networks_end[i] = [list_red, 32 - num_hosts]

print(sub_networks)
print(sub_networks_end)