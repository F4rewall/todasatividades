#Usando operadores matematicos
#print(1+1)
#print(10-1)
#print(100/20)
#print(1500*4)
"""
babigole
"""

#Aspas Simples
print("Matheus Araújo")
print(1, "Matheus")
print (123456789)
print (2, "Matheus 'Araujo'")
print ("Matheus \"Araujo\"")


#tipos de int e float
print (11)
print(-11)
print(0)

#float
print (1.1,10.11)
print(0.0, -1.5)

#tipos de dados
print(type('Matheus'))
print(type(0))
print(type(1.1))
print(type(2005-5-22))

#comparadores logicos
print (10 == 20)
print (10 == 10)
print(type(True))
print(type(True))

#STR,INTR,FLOAT. BOOL
print(int('1')), type(int('1'))
print(type (float(1) + 1))
print(bool(''))
print (str(11) + 'b' )

#criando variaveis
nome = 'Matheus'
nome2 = 'Maria'
soma = 2+2
idade = 18
maior_idade = idade >=18
data_nascimento = "22/05/2005"

print("Nome:", nome)
print("Soma:", soma)
print("Soma dobrada:", soma + soma)
print("Nome:", nome, "| Idade:", idade)
print("É maior de idade?", maior_idade)
print(nome, "tem", idade, "anos, nascido em", data_nascimento)

nome = input ('Digite o seu nome completo: ')
idade = int(input("Digite sua idade: "))
altura = float(input("Digite a sua altura: "))
resposta = input("Você está matriculado em qual curso? (sim/não):")
matriculado = resposta.lower() in ["sim", "s"]

print("\n--- DADOS CADASTRADOS ---")
print(f"Nome: {nome}")
print(f"Idade: {idade}")
print(f"Altura: {altura:}m")

if matriculado:
    print("Status da Matricula:Matriculado em um curso")
else:
    print("Status da Matricula:Não matriculado")
