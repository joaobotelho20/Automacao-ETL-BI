import os
import sys
import logging

# Adiciona a pasta src ao sys.path para permitir importações
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(SRC_PATH)

# Importa os módulos e renomeia os main() para melhor clareza
from extract_acadweb import main as extract_main
from transform import main as transform_main
from transform_comercial import main as transform_comercial_main
from utils import configurar_logging  # se você estiver usando

def run_pipeline():

    configurar_logging(path=r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\logs\ETL.log', nivel=logging.INFO)
    logging.info("Iniciando pipeline ETL via funcoes main()")

    # Etapa 1: Extração
    logging.info("Extracao iniciada")
    extract_main()

    # Etapa 2: Transformação
    logging.info("Transformacao iniciada")
    transform_main()

    # Etapa 3: Transformação Comercial
    logging.info("Transformacao Comercial iniciada")
    transform_comercial_main()

    logging.info("Pipeline ETL finalizada com sucesso")

if __name__ == "__main__":
    run_pipeline()
