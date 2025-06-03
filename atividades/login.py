print("""
  ,--,                                             
,--.'|                         ,--,                
|  | :     ,---.             ,--.'|         ,---,  
:  : '    '   ,'\   ,----._,.|  |,      ,-+-. /  | 
|  ' |   /   /   | /   /  ' /`--'_     ,--.'|'   | 
'  | |  .   ; ,. :|   :     |,' ,'|   |   |  ,"' | 
|  | :  '   | |: :|   | .\\  .'  | |   |   | /  | | 
'  : |__'   | .; :.   ; ';  ||  | :   |   | |  | | 
|  | '.'|   :    |'   .   . |'  : |__ |   | |  |/  
;  :    ;\\   \\  /  `---`-'| ||  | '.'||   | |--'   
|  ,   /  `----'   .'__/\\_: |;  :    ;|   |/       
 ---`-'            |   :    :|  ,   / '---'        
                    \\   \\  /  ---`-'               
                     `--`-'                        
""")



user = "matheus"
password = "10282226"
tentativas = 3

for i in range(tentativas):
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    if usuario == user and senha == password:
        print("Login bem-sucedido!")
        break
    else:
        print("Usuário ou senha incorretos.")
        restante = tentativas - i - 1
        if restante > 0:
            print(f"Tentativas restantes: {restante}")
        else:
            print("Conta bloqueada por excesso de tentativas.")

