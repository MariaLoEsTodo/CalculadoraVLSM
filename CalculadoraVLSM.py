"""CALCULADORA VSML MARÍA

Integrantes:
    - Juan Sebastián Barreto Jimenéz
    - Janet Chen He
    - María José Niño Rodriguez
    - David Santiago Quintana Echavarria

"""
#Librerías
import numpy as np
import math

#Funcion que convierte un numero decimal a binario
def decimal_to_binary(number, n_format='8'):
    s_format = '0' + n_format + 'b'
    return format(number,s_format)

#Funcion que convierte un numero binario a decimal
def binary_to_decimal(number_binary):
    return int(number_binary,2)

#Funcion que separa la dirección en cada octeto por "."
def split_base_address(base_address):
    return list(map(int, base_address.split(".")))

#Función que genera la mascara de red a partir del prefijo de red ingresado
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

#Función que valida la dirrección IP base sea de red
def validate_red_address(list_base_address, network_prefix):
    mask = build_mask(network_prefix)
    mask_np = np.array(mask)
    list_base_address_np = np.array(list_base_address)
    list_validate_address = list_base_address_np & mask_np
    print(list_validate_address, "otre", list_base_address_np)
    comparate = 0
    for i in range(4):
        if list_validate_address[i] == list_base_address_np[i]:
            comparate += 1
    if comparate == 4:
        return True
    else:
        return False

def validate_red_hosts(number_networks, net_num, number_prefix, sub_hosts, cont=0):
    if number_networks == 0:
        return True
    if cont == 0:
        net_num = 2**(32 - number_prefix - sub_hosts[cont][1])-1
    else: 
        if sub_hosts[cont][1] - sub_hosts[cont-1][1] == 0:
            net_num -= 1
        else:
            net_num += (2**(32 - number_prefix - (sub_hosts[cont][1]- sub_hosts[cont-1][1]))-1)
    if net_num == 0:
        return False
    validate_red_hosts(number_networks-1,net_num,number_prefix,sub_hosts,cont+1)
    

"""*****No sirve con otra dirección probe con 128.128.128.0/17 y da raro con 
    red 1 : 4000 host
    red 2 : 2500 host
    red 3 : 3000 host
  Si ordena pero saca mal el cálculo"""
  
#Se lee la dirección IP base
base_address = "200.200.200.0" #input("Ingrese la dirección IP base: ")
list_base_address = split_base_address(base_address)
print(list_base_address)

#Se lee el prefijo de red
network_prefix = 23 #int(input("Ingrese el prefijo de red: "))

#Se lee el numero de redes
number_networks = 6 #int(input("Ingrese el número de redes: "))
number_networks_bits = []

"""*****Borre el exit() porque entraba pero salía error, lo cambie por el else"""

# Validar la dirección dirección IP base
if(not(validate_red_address(list_base_address,network_prefix))):
    print("La dirección no es de red, vuelva a intentar")
    exit()
sub_hosts = {}

#for i in range(number_networks):
#    number_hosts = int(input("Ingrese el número de hosts de la red %d: " % i))
#    sub_hosts[i] = [number_hosts, math.ceil(math.log2(number_hosts +2))]
sub_hosts[0] = [200,8]
sub_hosts[1] = [120,7]
sub_hosts[2] = [62,6]
sub_hosts[3] = [28,5]
sub_hosts[4] = [13,4]
sub_hosts[5] = [2,2]
# sub_hosts[0] = [4000,12]
# sub_hosts[1] = [2500,12]
# sub_hosts[2] = [3000,12]


#Ordenar los subredes de mayor a menor 
for i in range(number_networks):
    number_networks_bits.append(32 - sub_hosts[i][1] + network_prefix)
sub_hosts = sorted(sub_hosts.items(),key=lambda x: x[1], reverse=True)

sub_networks = {}
sub_networks_end = {}

"""*****De acá para abajo no revise"""

for i  in range(number_networks):
    num_hosts = sub_hosts[i][1][1] #[subred id, num bit sub, mascara]
    bit_sub = 32 - network_prefix - num_hosts
    id_sub = ""
    if i == 0:
        for j in range(bit_sub):
            id_sub += '0'
        bit_sub_base = bit_sub
    else:
        id_sub_prev, bit_sub_prev, mask_sub_prev  = sub_networks[i-1]
        if bit_sub-bit_sub_prev == 0:
            aux_sum = binary_to_decimal(id_sub_prev)+1
        else:
            aux_sum = (2**(bit_sub)) - (2**(bit_sub-bit_sub_prev))
        if math.ceil(math.log2(aux_sum)) > number_networks_bits[i]:
            print("No es posible realizar más redes con los hosts indicados")
            exit()
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
    sub_networks_end[i] = [list_red, 32 - num_hosts]

print(sub_networks_end)