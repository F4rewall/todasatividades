import pyautogui
import time

def espera(segundos=2):
    time.sleep(segundos)

def clique(x,y,delay=2):
    print(f"Clicando em ({x},{y}) após {delay}s")
    espera(delay)
    pyautogui.click(x = x, y = y)

def doiscliques(x,y,delay=2):
    print(f"Dando dois cliques em ({x},{y}) após {delay}s")
    espera(delay)
    pyautogui.doubleClick(x = x, y = y) 

def abrir_site(nome_site, delay=2):
    espera(delay)
    pyautogui.write(nome_site)
    espera(delay)
    pyautogui.press('enter') 
    espera(3)

# sequência
clique(1801, 20)          
doiscliques(28, 938)     
clique(1862,21)
abrir_site('https://www.to.senac.br/')
clique(1183, 202)
clique(1209, 367)




