import pyautogui
import subprocess
import time
import pygetwindow as gw
from datetime import datetime, timedelta
import logging
from utils import obter_credenciais, configurar_logging, detectar_e_aceitar_popup

configurar_logging(path='ETL.log', nivel=logging.INFO)

pyautogui.FAILSAFE = True

software_path = r"C:\QualinfoCloud\acadwebcursos.exe"
subprocess.Popen(software_path)
time.sleep(5)

# (Opcional) Ativar a janela se souber o título
janela = gw.getWindowsWithTitle("acadwebcursos")[0]
janela.activate()
time.sleep(2)


email, senha = obter_credenciais("EMAIL", "SENHA", dotenv_path=r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\config\credenciais.env')

pyautogui.doubleClick(x=853, y=370)  # ajuste a posição do campo de usuário
pyautogui.PAUSE = 1
pyautogui.write(email, interval=0.06)
# pyautogui.click(x=716, y=396)
pyautogui.press('tab')
pyautogui.write(senha, interval=0.06)
pyautogui.press('enter')
time.sleep(2)
pyautogui.press('enter')  # entrando unidade
time.sleep(3)
detectar_e_aceitar_popup(imagem_popup= r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\src\popup_login.png', timeout = 3, intervalo = 0.5)


time.sleep(10)
pyautogui.press('esc')  # removendo popup de aviso inicial

pyautogui.hotkey('alt', 'a')
pyautogui.press('a')
time.sleep(5)
pyautogui.click(x=184, y=686)  # relatorio botao
time.sleep(3)
pyautogui.write("101", interval=0.1)
pyautogui.hotkey('alt', 'r')  # executando relatorio analitico 101

# defininco intervao de busca
hoje = datetime.today()
ontem = datetime.today() - timedelta(days=1)
ontem_formatado = ontem.strftime('%d%m%Y')
primeiro_dia_mes_anterior = hoje.replace(month=hoje.month - 1, day=1)
primeiro_dia_mes_anterior_formatado = primeiro_dia_mes_anterior.strftime('%d%m%Y')

pyautogui.press('tab', presses=2, interval=0.5)
pyautogui.write(primeiro_dia_mes_anterior_formatado, interval=0.1)  # data inicial
pyautogui.press('tab')
pyautogui.write(ontem_formatado, interval=0.1)  # data inicial
pyautogui.press('tab')
pyautogui.write(ontem_formatado, interval=0.1)  # data inicial

pyautogui.click(x=1024, y=639)
time.sleep(8)

pyautogui.click(x=308, y=39)  # botao de impressaora para gerar excel
pyautogui.press('tab', presses=2, interval=0.5)
pyautogui.press('down')
pyautogui.press('tab', presses=2, interval=0.5)
pyautogui.press('enter')
time.sleep(3)

pyautogui.write('evasao_mes_atual', interval=0.1)
pyautogui.press('tab', presses=7, interval=0.5)
pyautogui.press('enter')
time.sleep(2)
pyautogui.write(r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\raw', interval=0.1)
pyautogui.press('enter')
pyautogui.hotkey('alt', 'l')

pyautogui.hotkey('alt', 's')
time.sleep(3)

# fechando software
pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('alt', 'f4')
pyautogui.press('enter')  # confirmando fechamento
logging.info("Acadweb finaliazdo com sucesso")
