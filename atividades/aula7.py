x = 1
while x <=5:
    print(x)
    x = x + 1

x = 50
while x <= 100:
    print(x)
    x = x + 1

x = 10
while x >= 0:
    print(x)
    x = x - 1

print("Foguete lançado!")

x = 10
while x <= 100:
     if x % 2 == 0:
        print(x)
     x += 2

n = int(input("Escolha um número: "))

x = 2
while x <= n:
    print(x)
    x += 2

senha = ""

while senha != "senac":
    senha = input("Digite a senha: ")
    if senha != "senac":
        print("Senha incorreta. Tente novamente.")

print("Acesso liberado.")
