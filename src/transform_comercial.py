import pandas as pd
import logging
from utils import normalizar_texto, padronizar_datas, configurar_logging

def main():
    configurar_logging(path=r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\logs\ETL.log', nivel=logging.INFO)

    df = pd.read_excel(r"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\raw\comercial_analitico.xls",)

    df = df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 6','Unnamed: 7'])
    df = df.dropna(how='all')

    col_data = [col for col in df.columns if col.startswith("Data :")]
    if col_data:
        df = df.drop(col_data, axis=1)

    df = df.rename(columns={
        'Unnamed: 3': 'orientador',
        'Unnamed: 4': 'curso',
        'Unnamed: 5': 'matricula',
        'Unnamed: 8': 'data'
    })

    valores_indesejados = ['Orientador', 'Curso', 'Matricula', 'Data Mat.']
    df = df[~df.apply(lambda row: row.astype(str).isin(valores_indesejados).any(), axis=1)]
    df = df.dropna(how='all')

    df['data'] = df['data'].astype(str)
    df = padronizar_datas(df, coluna='data')

    df['orientador'] = df['orientador'].apply(normalizar_texto)
    df['curso'] = df['curso'].apply(normalizar_texto)
    df['matricula'] = df['matricula'].apply(normalizar_texto)
    df['orientador'] = df['orientador'].apply(normalizar_texto)
    df.reset_index(drop=True, inplace=True)

    df[['codigo', 'orientador']] = df['orientador'].str.split(' - ', expand=True)
    df[['matricula', 'aluno']] = df['matricula'].str.split(' - ', expand=True)
    df['matricula'] = df['matricula'].str.upper()
    df['nome_curso'] = df['matricula'].str.replace(r'[^a-zA-Z]', '', regex=True)

    df.to_excel(fr"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\processed\comercial_analitico.xlsx", index=False)

if __name__ == "__main__":
    main()
