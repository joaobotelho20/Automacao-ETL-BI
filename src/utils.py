import os
from dotenv import load_dotenv
import logging
import pyautogui
import time
from pyautogui import ImageNotFoundException

def obter_credenciais(*nomes_variaveis, dotenv_path=None):
    """
    Lê as variáveis de ambiente definidas em um arquivo `.env` e retorna os valores na mesma ordem.
    
    Args:
        *nomes_variaveis (str): nomes das variáveis de ambiente que devem ser buscadas, podem ser passados vários nomes.
        dotenv_path (str, opcional): caminho para o arquivo .env a ser carregado. Se None, carrega o caminho que o módulo dessa funçao está.

    Retorna:
        tuple: uma tupla com os valores das variáveis passadas.

    Exceções:
        Levanta ValueError se alguma das variáveis não estiver definida.
    """
    if dotenv_path is None:
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path) 

    valores = []
    for nome in nomes_variaveis:
        valor = os.getenv(nome)
        if not valor:
            raise ValueError(f"{nome} não está definido no arquivo .env")
        valores.append(valor)

    return tuple(valores)

def configurar_logging(path: str = 'default.log', nivel: int = logging.INFO) -> None:
    """
    Configura o logging básico para o script.


    Args:
        path (str): Caminho (e nome) do arquivo onde os logs serão salvos. Default é 'default.log'.
        nivel (int): Nível mínimo do log (ex: logging.INFO, logging.DEBUG, logging.ERROR). Default é logging.INFO.

    Retorna:
        None
    """
    logging.basicConfig(
        filename=path,
        level=nivel,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def detectar_e_aceitar_popup(imagem_popup: str, timeout: int = 10, intervalo: float = 0.5) -> bool:
    """
    Detecta a presença de um pop-up na tela baseado em uma imagem e pressiona Enter quando encontrado.

    Args:
        imagem_popup (str): Caminho para a imagem do pop-up que será usada para detecção.
        timeout (int): Tempo máximo em segundos para aguardar o aparecimento do pop-up.
        intervalo (float): Intervalo em segundos entre tentativas de detecção.

    Returns:
        bool: True se o pop-up foi detectado e Enter pressionado, False se o tempo expirou ou ocorreu erro.
    """
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        try:
            localizacao = pyautogui.locateOnScreen(imagem_popup, confidence=0.8)
            if localizacao is not None:
                pyautogui.press('enter')
                print("Pop-up detectado e Enter pressionado.")
                return True
        except ImageNotFoundException:
            # A imagem não foi localizada com confiança suficiente
            pass
        except Exception as e:
            print(f"Erro ao tentar detectar o pop-up: {e}")
            return False
        time.sleep(intervalo)
    
    print("Pop-up não detectado dentro do tempo limite.")
    return False