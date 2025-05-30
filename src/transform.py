import pandas as pd
import logging
from utils import normalizar_texto, padronizar_datas, configurar_logging

configurar_logging(path='ETL.log', nivel=logging.INFO)

df_list = ['evasao_mes_atual']

for df_name in df_list:

    df = pd.read_excel(fr"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\raw\{df_name}.xls",)
    df = df.drop(columns=['Unnamed: 0','Unnamed: 2','Unnamed: 4','Unnamed: 7','Unnamed: 9','Unnamed: 11'])
    df = df.dropna(how='all')

    col_data = [col for col in df.columns if col.startswith("Data :")]
    if col_data:
        df = df.rename(columns={col_data[0]: 'matricula'})

    df = df.rename(columns={
        'Unnamed: 3': 'nome',
        'Unnamed: 5': 'cpf',
        'Unnamed: 6': 'pagamento_matricula',
        'Unnamed: 8': 'orientador',
        'Unnamed: 10': 'data',
        'Unnamed: 12': 'situacao'
    })

    valores_indesejados = ['Matricula', 'Nome', 'CPF', 'Pgto. da Matrícula', 'Orientador', 'NaT', 'Situação']
    df = df[~df.apply(lambda row: row.astype(str).isin(valores_indesejados).any(), axis=1)]

    # Filtrar linhas onde 'col_ref' começa com "Data" e mascara para outros valores nas outras colunas
    mask_inicio_data = df['matricula'].astype(str).str.startswith(('Data', 'Hora', 'Página'))
    mask_outros_valores = df.drop(columns=['matricula']).isna().any(axis=1)
    df_filtrado = df[mask_inicio_data & mask_outros_valores]
    df = df[~df.isin(df_filtrado)]

    df = df[df['situacao'].notna() & (df['situacao'] != '')]

    df = padronizar_datas(df, coluna='data')

    df['nome'] = df['nome'].apply(normalizar_texto)
    df['cpf'] = df['cpf'].astype(str).str.replace('.', '', regex=False).str.replace('-', '', regex=False)
    df['situacao'] = df['situacao'].apply(normalizar_texto)
    df['orientador'] = df['orientador'].apply(normalizar_texto)
    df['pagamento_matricula'] = df['pagamento_matricula'].apply(normalizar_texto)
    df.reset_index(drop=True, inplace=True)

    df['status'] = df['situacao'].map({
        'cancelamento comercial': 'CAC',
        'cancelamento interno': 'CAI',
        'cancelamento normal': 'CAN',
        'cancelamento unidade': 'CAU',
        'formado': 'FO',
        'limpeza academica': 'LAC',
        'limpeza de frequencia': 'LFR',
        'limpeza financeira': 'LFI',
        'nao formados': 'NF',
        'nunca compareceu': 'NC',
        'transferencia interna': 'TF',
    })

    df['curso'] = df['matricula'].str.replace(r'[^a-zA-Z]', '', regex=True)

    df.to_excel(fr"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\processed\{df_name}.xlsx", index=False)