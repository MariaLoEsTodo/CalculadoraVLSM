from tabulate import tabulate
print("| Red | Hosts | Dirección de red |")
print ("{:<8} {:<15} {:<10}".format('Red','Hosts','Dirección de red'))

d = [ ["Mark", 12, 95],
     ["Jay", 11, 88],
     ["Jack", 14, 90]]

print(tabulate(d, headers=["Red", "Hosts", "Dirección de red"]))