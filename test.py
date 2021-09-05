def validate_red_hosts(number_networks, net_num, number_prefix, sub_hosts, cont=0):
    if number_networks == 0:
        return True
    if cont == 0:
        net_num = (2**(32 - number_prefix - sub_hosts[cont][1]))-1
    else: 
        if sub_hosts[cont][1] - sub_hosts[cont-1][1] == 0:
            net_num -= 1
        else:
            print("net num: int: ", net_num,"number_prefix:",number_prefix, "host:",sub_hosts[cont][1] )
            net_num += ((2**(32 - number_prefix - sub_hosts[cont][1]))-1)
            print("net num: int: ", net_num)
    print("net_num:", net_num, "cont=", cont, "number_networks", number_networks)
    if net_num == 0:
        return False
    validate_red_hosts(number_networks-1,net_num,number_prefix + net_num,sub_hosts,cont+1)

#Se lee el prefijo de red
network_prefix = 23 #int(input("Ingrese el prefijo de red: "))

#Se lee el numero de redes
number_networks = 6 #int(input("Ingrese el número de redes: "))
sub_hosts = {}
sub_hosts[0] = [200,8]
sub_hosts[1] = [120,7]
sub_hosts[2] = [62,6]
sub_hosts[3] = [28,5]
sub_hosts[4] = [13,4]
sub_hosts[5] = [2,2]

if validate_red_hosts(number_networks,0, network_prefix, sub_hosts):
    print("Valido")
else:
    print("NO valido")