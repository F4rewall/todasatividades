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

def escrever_gmail(gmailescrever, delay=2):
    espera(delay)
    pyautogui.write(gmailescrever)
    espera(delay)
    pyautogui.press('enter') 

def atividade(atividadeescrever, delay=2):
    espera(delay)
    pyautogui.write(atividadeescrever)
    espera(delay)

# sequência
clique(1801, 20)          
doiscliques(28, 938)     
clique(1862,21)
abrir_site('https:gmail.com')
clique(104,187)
clique(1427,1002)
clique(154,415)
clique(63,321)
doiscliques(321,179)
doiscliques(229,383)
doiscliques(224,216)
doiscliques(389,382)
doiscliques(278,216)
doiscliques(325,165)
doiscliques(334,192)
clique(279,333)
clique(782,501)
clique(1301,480)
escrever_gmail('mateusgn@to.senac.br')
clique(1765,539)
atividade('atividade de automação')
clique(1294,1001)

