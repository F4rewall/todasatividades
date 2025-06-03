# 1. Soma de dois números
a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
print("Soma:", a + b)

# 2. Verificador de número par ou ímpar
n = int(input("Digite um número: "))
print("Par" if n % 2 == 0 else "Ímpar")

# 3. Tabuada personalizada
n = int(input("Digite um número para ver a tabuada: "))
for i in range(1, 11):
    print(f"{n} x {i} = {n*i}")

# 4. Contador de vogais
palavra = input("Digite uma palavra: ").lower()
vogais = "aeiou"
cont = sum(1 for letra in palavra if letra in vogais)
print("Quantidade de vogais:", cont)

# 5. Média de notas
notas = [float(input(f"Digite a nota {i+1}: ")) for i in range(3)]
media = sum(notas)/3
if media >= 7:
    status = "Aprovado"
elif media >= 5:
    status = "Recuperação"
else:
    status = "Reprovado"
print("Média:", media, "-", status)

# 6. Lista de compras
lista = [input(f"Item {i+1}: ") for i in range(5)]
print("Lista de compras:", lista)

# 7. Verificador de palíndromo
palavra = input("Digite uma palavra: ").lower()
print("É palíndromo" if palavra == palavra[::-1] else "Não é palíndromo")

# 8. Calculadora simples
op = input("Escolha a operação (+, -, *, /): ")
a = float(input("Digite o primeiro número: "))
b = float(input("Digite o segundo número: "))
if op == '+': print("Resultado:", a + b)
elif op == '-': print("Resultado:", a - b)
elif op == '*': print("Resultado:", a * b)
elif op == '/': print("Resultado:", a / b if b != 0 else "Divisão por zero")
else: print("Operação inválida")

# 9. Números pares de 1 a 50
for i in range(2, 51, 2):
    print(i, end=' ')
print()

# 10. Cadastro de usuários
usuario = {
    "nome": input("Nome: "),
    "idade": int(input("Idade: ")),
    "email": input("Email: ")
}
print("Cadastro:", usuario)

# 11. Contador de números positivos e negativos
nums = [int(input(f"Número {i+1}: ")) for i in range(10)]
pos = sum(1 for x in nums if x > 0)
neg = sum(1 for x in nums if x < 0)
zero = nums.count(0)
print("Positivos:", pos, "Negativos:", neg, "Zeros:", zero)

# 12. Maior e menor número
numeros = [int(input(f"Número {i+1}: ")) for i in range(5)]
print("Maior:", max(numeros), "Menor:", min(numeros))

# 13. Contador de palavras
frase = input("Digite uma frase: ")
print("Quantidade de palavras:", len(frase.split()))

# 14. Gerador de senha aleatória
import random
import string
caracteres = string.ascii_letters + string.digits + string.punctuation
senha = ''.join(random.choice(caracteres) for _ in range(8))
print("Senha gerada:", senha)

# 15. Fatorial de um número
n = int(input("Digite um número para o fatorial: "))
fat = 1
for i in range(2, n+1):
    fat *= i
print(f"{n}! =", fat)

# 16. Verificador de número primo
n = int(input("Digite um número: "))
if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5)+1)):
    print("É primo")
else:
    print("Não é primo")

# 17. Conversor de temperatura
c = float(input("Temperatura em Celsius: "))
f = (c * 9/5) + 32
print("Temperatura em Fahrenheit:", f)

# 18. Agenda de contatos
agenda = {}
for i in range(3):
    nome = input(f"Nome do contato {i+1}: ")
    telefone = input(f"Telefone do contato {i+1}: ")
    agenda[nome] = telefone
print("Agenda:", agenda)

# 19. Contagem regressiva com tempo
import time
n = int(input("Digite um número para contagem regressiva: "))
for i in range(n, -1, -1):
    print(i)
    time.sleep(1)

# 20. Verificador de CPF simples
cpf = input("Digite o CPF (somente números): ")
print("CPF válido" if cpf.isdigit() and len(cpf) == 11 else "CPF inválido")