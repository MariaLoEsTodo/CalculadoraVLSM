import numpy as np
import math

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
    print(list_base_address)
    print(mask)
    mask_np = np.array(mask)
    list_base_address_np = np.array(list_base_address)
    list_validate_address = list_base_address_np & mask_np
    comparate_lists = [item for item in list_base_address if item in list_validate_address]
    return len(comparate_lists) == 4

# se lee dirección IP base
base_address = "192.168.0.0" #input("Ingrese la dirección IP base: ")
list_base_address = split_base_address(base_address)
print(list_base_address)
# se lee el prefijo de red
network_prefix = 26 #int(input("Ingrese el prefijo de red: "))
# se lee el numero de redes
number_networks = 2 #int(input("Ingrese el número de redes: "))
number_networks_bits = math.ceil(math.log2(number_networks))

print(number_networks_bits)

# validate red base address
if(not(validate_red_address(list_base_address,network_prefix))):
    print("La dirección no es de red, vuelva a intentar")
    exit()

sub_hosts = {}

#for i in range(number_networks):
#    number_hosts = int(input("Ingrese el número de hosts de la red %d: " % i))
#    sub_hosts[i] = [number_hosts, math.ceil(math.log2(number_hosts +2))]
sub_hosts[0] = [23,3]
sub_hosts[1] = [456,5]
sub_hosts = sorted(sub_hosts.items(),key=lambda x: x[1], reverse=True)

possible = True
for i in range(number_networks):   
    if( (sub_hosts[i][1][1] + number_networks_bits + network_prefix) > 32):
        possible=False
        print("No es posible generar su redes")

sub_networks = {}
        
if(possible == True):
    for i  in range(number_networks):  
        sub_networks[i] = [i , 32 - sub_hosts[i][1][1] ]
        
print (sub_networks)
    










