# Parte 1 — Pesquisa

# 1. Conceito de estruturas de decisão em Python:
"""
Estruturas de decisão permitem que o programa tome caminhos diferentes
dependente de condições lógicas. Usamos o if, elif e else para isso.
Exemplo: verificar se um número é positivo ou negativo.
"""
num = int(input("Digite um número: "))
if num > 0:
    print("Positivo")
elif num < 0:
    print("Negativo")
else:
    print("Zero")

# 2. Diferenças entre estruturas simples, compostas e encadeadas
# Decisão Simples
idade = 18
if idade >= 18:
    print("Maior de idade")

# Decisão Composta
if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")

# Decisão Encadeada
if idade < 12:
    print("Criança")
elif idade < 18:
    print("Adolescente")
else:
    print("Adulto")

# 3. Operadores relacionais e lógicos
# Relacionais: >, <, >=, <=, ==, !=
# Lógicos: and, or, not
# Exemplo com operadores lógicos:
nota = 7
faltas = 3
if nota >= 6 and faltas <= 5:
    print("Aprovado")

# 4. Erro comum: esquecer a indentação
# Errado:
"""
if True:
print("Erro de indentação")
"""
# Correto:
if True:
    print("Indentação correta")

# Parte 2 — Prática

# Atividade 1: Sistema de Cadastro de Filmes
classificacao = int(input("Classificação indicativa do filme: "))
if classificacao <= 10:
    print("Filme infantil")
elif classificacao in [12, 13]:
    print("Filme para pré-adolescentes")
elif classificacao in [14, 15, 16]:
    print("Filme para adolescentes")
elif classificacao in [17, 18]:
    print("Filme para adultos")
elif classificacao > 18:
    print("Classificação não reconhecida")

# Atividade 2: Avaliação de nota
nota = float(input("Informe a nota (0 a 10): "))
if nota < 6:
    print("Reprovado")
elif nota < 7.5:
    print("Recuperação")
else:
    print("Aprovado")

# Atividade 3: Análise de temperatura
temp = float(input("Informe a temperatura: "))
if temp < 10:
    print("Muito frio")
elif temp <= 25:
    print("Clima agradável")
else:
    print("Muito quente")
