# meus_produtos = {"mouse": 150,"teclado": 200,"monitor": 800,"gabinete": 500}
#mostre todos os produtos e seus preços
meus_produtos = {"mouse": 150, "teclado": 200, "monitor": 800, "gabinete": 500}

# Mostrar todos os produtos e seus preços
print("\nLista de produtos disponíveis:")
for nome, preco in meus_produtos.items():
    print(f"{nome}: R$ {preco:.2f}")

# Mostrar o preço de um produto específico
produto = input("\nDigite o nome do produto para ver o preço: ")
if produto in meus_produtos:
    print(f"O preço do {produto} é R$ {meus_produtos[produto]:.2f}")
else:
    print("Produto não encontrado.")

# Atualizar o preço de um produto
produto_atualizar = input("\nDigite o nome do produto que deseja atualizar o preço: ")
if produto_atualizar in meus_produtos:
    novo_preco = float(input(f"Digite o novo preço do {produto_atualizar}: R$ "))
    meus_produtos[produto_atualizar] = novo_preco
    print(f"Preço do {produto_atualizar} atualizado para R$ {novo_preco:.2f}")
else:
    print("Produto não encontrado para atualização.")

# Adicionar um novo produto
novo_produto = input("\nDigite o nome de um novo produto para adicionar: ")
if novo_produto in meus_produtos:
    print("Este produto já existe.")
else:
    preco_novo_produto = float(input(f"Digite o preço do {novo_produto}: R$ "))
    meus_produtos[novo_produto] = preco_novo_produto
    print(f"Produto {novo_produto} adicionado com sucesso!")

# Remover um produto
remover_produto = input("\nDigite o nome do produto que deseja remover: ")
if remover_produto in meus_produtos:
    del meus_produtos[remover_produto]
    print(f"Produto {remover_produto} removido com sucesso.")
else:
    print("Produto não encontrado para remoção.")

# Mostrar lista final de produtos
print("\nProdutos atualizados:")
for nome, preco in meus_produtos.items():
    print(f"{nome}: R$ {preco:.2f}")

