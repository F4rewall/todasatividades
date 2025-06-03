# soma = 0

# while True:
#     numero = float(input("Digite um numero para somar ou 0 para sair"))
#     if numero == 0:
#         break
#     soma += numero
# print(f"A soma de todos os numeros digitados é {soma}")    

while True:
    try:
        idade = int(input("Digite uma idade: "))
    except ValueError:
        print("Por favor, digite um número inteiro válido para a idade.")
        continue

    if idade >= 18:
        print("Acesso à festa concedido")
    elif idade < 18:
        print("Entrada negada")

    while True:
        continuar = input("Deseja verificar mais alguma idade? [S ou N]: ").strip().upper()
        if continuar == 'S':
            break
        elif continuar == 'N':
            print("Encerrando o programa. Até mais!")
            exit()
        else:
            print("Opção inválida. Por favor, digite apenas S ou N.")
