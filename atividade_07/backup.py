# import os

# from tkinter.filedialog import askdirectory
# import shutil

# pasta_selecionada = askdirectory()
# print(pasta_selecionada)


# lista_arquivos = os.listdir(pasta_selecionada)
# print(lista_arquivos)
# nome_pasta_backup = 'backup'
# nome_completo_backup = f'{pasta_selecionada}/{nome_pasta_backup}'
# if not os.path.exists(nome_completo_backup):
#     os.mkdir(nome_completo_backup)

# for arquivos in lista_arquivos:
#     print(arquivos)
#     nome_arquivo_completo = f'{pasta_selecionada} / {arquivos}' 
#     nome_final_arquivo = f'{nome_completo_backup}/{arquivos}'
# if '.' in arquivos:
#     shutil.copy2(nome_arquivo_completo,nome_final_arquivo)
# elif 'backup' != arquivos:  
#     shutil.copytree(nome_arquivo_completo,nome_final_arquivo)



import os
from tkinter.filedialog import askdirectory
import shutil
import datetime
import time

# Função para criar o nome da pasta de backup com data e hora
def get_backup_folder_name():
    now = datetime.datetime.now()
    return f"backup_{now.strftime('%Y-%m-%d_%H-%M-%S')}"

# Função para realizar o backup
def perform_backup(source_folder):
    # Nome da nova pasta de backup
    backup_folder_name = get_backup_folder_name()
    backup_folder_path = os.path.join(source_folder, backup_folder_name)

    # Cria a pasta de backup
    os.makedirs(backup_folder_path, exist_ok=True)
    print(f"Pasta de backup criada: {backup_folder_path}")

    # Lista todos os arquivos e pastas dentro da pasta selecionada
    items_to_copy = os.listdir(source_folder)

    print(f"Iniciando backup da pasta: {source_folder}")

    # Itera sobre cada item na pasta de origem
    for item in items_to_copy:
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(backup_folder_path, item)

        # Ignora a própria pasta de backup
        if item == os.path.basename(backup_folder_path):
            continue

        print(f"Processando: {item}")

        # Se for um arquivo, copia como arquivo
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)

        # Se for uma pasta, copia recursivamente
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)

    print(f"Backup concluído para a pasta: {backup_folder_path}")

# Loop principal
while True:
    print("\nSelecione a pasta que deseja fazer backup...")
    pasta_selecionada = askdirectory(title="Selecione a pasta para backup")

    if not pasta_selecionada:
        print("Nenhuma pasta selecionada. Tentando novamente em 60 segundos.")
        time.sleep(60)
        continue

    print(f"\nPasta selecionada: {pasta_selecionada}")
    
    try:
        # Realiza o primeiro backup
        perform_backup(pasta_selecionada)

        # Aguarda 5 minutos antes do próximo backup
        print("\nPróximo backup será feito em 5 minutos...\n")
        time.sleep(300)  # 300 segundos = 5 minutos

    except Exception as e:
        print(f"Ocorreu um erro durante o backup: {e}")
        time.sleep(60)  # Espera 1 minuto antes de tentar novamente