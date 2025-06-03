#Criando Listas
estados = ["TO", "SP", "RJ"]

print(estados)

print (estados[0])
print (estados[1])
print (estados[2])

estados =["TO", "SP", "RJ"]
estados.append("PA")
estados.remove ("RJ") #Remove Itens da lista
print (estados)

estados =["TO", "SP", "RJ"]
for estados in estados:
    print (f"Òla, {estados}")