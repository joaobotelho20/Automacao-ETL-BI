import pyautogui
import subprocess
import time
import pygetwindow as gw
import pyperclip

software_path = r"C:\QualinfoCloud\acadwebcursos.exe"
subprocess.Popen(software_path)
time.sleep(5)

# (Opcional) Ativar a janela se souber o título
janela = gw.getWindowsWithTitle("acadwebcursos")[0]
janela.activate()
time.sleep(2)

pyautogui.PAUSE = 1
# Digitar o nome de usuário
pyautogui.doubleClick(x=853, y=370)  # ajuste a posição do campo de usuário
pyautogui.write("julia.martins.lc@gmail.com", interval=0.1)

pyautogui.click(x=716, y=396)  # ajuste a posição do campo de senha
pyautogui.write("360702",interval=0.1)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')
time.sleep(10)
pyautogui.press('esc')

pyautogui.hotkey('alt', 'a')     
pyautogui.press('a')
time.sleep(5)
pyautogui.click(x=184, y=686)  # relatorio botao
time.sleep(3)
pyautogui.write("101",interval=0.1)
pyautogui.hotkey('alt', 'r') 

pyautogui.press('tab', presses=2, interval=0.5)  
pyperclip.copy('01/05/2025')
pyautogui.hotkey('ctrl', 'v') 
pyautogui.press('tab')

pyperclip.copy('31/05/2025')
pyautogui.hotkey('ctrl', 'v') 
pyautogui.press('tab')
pyautogui.hotkey('ctrl', 'v') 

pyautogui.click(x=1024, y=639)
time.sleep(8)

pyautogui.click(x=308, y=39)
pyautogui.press('tab', presses=2, interval=0.5)  
pyautogui.press('down')  
pyautogui.press('tab', presses=2, interval=0.5)  
pyautogui.press('enter')  
time.sleep(3)

pyautogui.write('evasao_analitico_maio_2025',interval=0.1)
pyautogui.press('tab', presses=7, interval=0.5)  
pyautogui.press('enter')
time.sleep(2)
pyautogui.write(r'c:\Users\USER\Desktop',interval=0.1)
pyautogui.press('enter')
pyautogui.hotkey('alt', 'l') 