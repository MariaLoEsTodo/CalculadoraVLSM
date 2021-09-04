def decimal_to_binary(number):
    return int(format(number,"b"))

def binary_to_decimal(number_binary):
    return int(number_binary,2)

def split_base_address(base_address):
    return list(map(int, base_address.split(".")))

# se lee dirección IP base
base_address = "192.168.0.1" #input("Ingrese la dirección IP base: ")
list_base_address = split_base_address(base_address)
print(list_base_address)
binary_list_base_address = []
for i in range(4):
    binary_list_base_address.append(decimal_to_binary(list_base_address[i]))
print(binary_list_base_address)
# se lee el prefijo de red
network_prefix = 24 #int(input("Ingrese el prefijo de red: "))
# se lee el numero de redes
number_networks = 5 #int(input("Ingrese el número de redes: "))