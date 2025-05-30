import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Now your existing imports
from src.extract_acadweb import main as main_extract


import logging
from src.extract_acadweb import main as main_extract
from src.transform import main as main_transform
from src.utils import configurar_logging

def pipeline_etl():
    """Orquestrador principal do fluxo ETL"""
    logging.info("Iniciando pipeline ETL")
    
    try:
        logging.info("Iniciando extração de dados")
        main_extract()  # Chamada direta da função importada
        logging.info("Extração concluída com sucesso")
        
    except Exception as e:
        logging.error(f"Erro na extração: {e}", exc_info=True)
        return

    try:
        logging.info("Iniciando transformação de dados")
        main_transform()  # Chamada direta da função importada
        logging.info("Transformação concluída com sucesso")
        
    except Exception as e:
        logging.error(f"Erro na transformação: {e}", exc_info=True)
        return

    logging.info("Pipeline ETL finalizado com sucesso")

if __name__ == "__main__":
    configurar_logging(path='ETL.log', nivel=logging.INFO)
    pipeline_etl()