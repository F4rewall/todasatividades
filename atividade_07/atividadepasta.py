import os

lista_arquivos = os.listdir("documentos")

print(lista_arquivos)

for arquivo in lista_arquivos:
    if '.doc' in arquivo or '.docx' in arquivo:
        os.rename(f"documentos/{arquivo}", f"documentos/word/{arquivo}")
    
    elif '.xls' in arquivo or '.xlsx' in arquivo:
        os.rename(f"documentos/{arquivo}", f"documentos/excel/{arquivo}")
    
    elif '.pptx' in arquivo or '.pptx' in arquivo:
        os.rename(f"documentos/{arquivo}", f"documentos/powerpoint/{arquivo}")
