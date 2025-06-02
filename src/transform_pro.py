import pandas as pd
import logging
from utils import normalizar_texto, padronizar_datas, configurar_logging



configurar_logging(path=r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\logs\ETL.log', nivel=logging.INFO)

df = pd.read_excel(r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\raw\pro_matriculas_recebidas.xls')

df = df.drop(columns=['Unnamed: 3','Unnamed: 5','Unnamed: 8','Unnamed: 12','Unnamed: 13','Unnamed: 17','Unnamed: 24'])
df = df.dropna(how='all')
df = df.dropna(axis=1, how='all')

col_data = [col for col in df.columns if col.startswith("Data :")]
if col_data:
    df = df.rename(columns={col_data[0]: 'curso'})

df = df.rename(columns={
    'Unnamed: 2': 'matricula',
    'Unnamed: 4': 'nome',
    'Unnamed: 9': 'turma',
    'Unnamed: 10': 'data_mat',
    'Unnamed: 11': 'taxa',
    'Unnamed: 18': 'valor',
    'Unnamed: 19': 'desc_percentual',
    'Unnamed: 20': 'data_pagto',
    'Unnamed: 21': 'desc_pagto',
    'Unnamed: 22': 'valor_pagto',
    'Unnamed: 23': 'plano_do_aluno',
    'Unnamed: 27': 'valor_mensalidade',
    'Unnamed: 28': 'desc_mensalidade'
})

valores_indesejados = ['Curso', 'Matrícula', 'Nome', 'Turma', 'Dt. Matr.', 'Taxa', 'Valor', 'Desc. (%)', 'Data Pagto', 'Desc. Pagto', 'Valor Pagto', 'Plano do Aluno', 'Valor', 'Desc. (%)']
df = df[~df.apply(lambda row: row.astype(str).isin(valores_indesejados).any(), axis=1)]

# Filtrar linhas onde 'col_ref' começa com "Data" e mascara para outros valores nas outras colunas
mask_inicio_data = df['curso'].astype(str).str.startswith(('Data da Baixa', 'Hora', 'Página','Matrículas Efetuadas'))
mask_outros_valores = df.drop(columns=['curso']).isna().any(axis=1)
df_filtrado = df[mask_inicio_data & mask_outros_valores]
df = df[~df.isin(df_filtrado)]

df = df.dropna(how='all')

contagem_nao_nan = df.notna().sum(axis=1)
df= df[~(contagem_nao_nan <= 5)]

df[['data_mat','data_pagto']] = df[['data_mat','data_pagto']].astype(str)
df = padronizar_datas(df, coluna='data_mat')
df = padronizar_datas(df, coluna='data_pagto')

df['desc_percentual'] = df['desc_percentual'].str.rstrip('%').astype(float) / 100
df['desc_mensalidade'] = df['desc_mensalidade'].str.rstrip('%').astype(float) / 100

df = df.groupby('matricula', as_index=False).agg({
    'desc_pagto': 'sum',
    'valor_pagto': 'sum',
    'nome': 'first',
    'turma': 'first',
    'curso': 'first',
    'matricula': 'first',
    'nome': 'first',
    'turma': 'first',
    'data_mat': 'first',
    'taxa': 'first',
    'valor': 'first',
    'desc_percentual': 'first',
    'data_pagto': 'first',
    'plano_do_aluno': 'first',
    'valor_mensalidade': 'first',
    'desc_mensalidade': 'first',
})

df.reset_index(drop=True, inplace=True)

df_2 = df.copy()

df = pd.read_excel(r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\raw\pro_situacao_analitico.xls')

df = df.drop(columns=['Unnamed: 5','Unnamed: 9','Unnamed: 11'])
df = df.dropna(how='all')
df = df.dropna(axis=1, how='all')

col_data = [col for col in df.columns if col.startswith("Data :")]
if col_data:
    df = df.rename(columns={col_data[0]: 'matricula'})

df = df.rename(columns={
    'Unnamed: 3': 'nome',
    'Unnamed: 6': 'pagto_mat',
    'Unnamed: 8': 'orientador',
    'Unnamed: 10': 'data_evasao',
    'Unnamed: 12': 'situacao',
})

valores_indesejados = ['Matricula','Nome','Pgto. da Matrícula','Orientador','NaT','Situação']
df = df[~df.apply(lambda row: row.astype(str).isin(valores_indesejados).any(), axis=1)]

# Filtrar linhas onde 'col_ref' começa com "Data" e mascara para outros valores nas outras colunas
mask_inicio_data = df['matricula'].astype(str).str.startswith(('Período', 'Hora', 'Página','Listagem de Alunos'))
mask_outros_valores = df.drop(columns=['matricula']).isna().any(axis=1)
df_filtrado = df[mask_inicio_data & mask_outros_valores]
df = df[~df.isin(df_filtrado)]

df['data_evasao'] = df['data_evasao'].astype(str)
df = padronizar_datas(df, coluna='data_evasao')

df['nome'] = df['nome'].apply(normalizar_texto)
df['pagto_mat'] = df['pagto_mat'].apply(normalizar_texto)
df['orientador'] = df['orientador'].apply(normalizar_texto)
df['situacao'] = df['situacao'].apply(normalizar_texto)

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
    'matriculado': 'MT',
})

df.reset_index(drop=True, inplace=True)

df_merged = pd.merge(df, df_2, on='matricula', how='left', suffixes=('', '_right'))
df_merged = df_merged.drop(columns=['nome_right'])
df_merged['nome_curso'] = df_merged['matricula'].str.replace(r'[^a-zA-Z]', '', regex=True)


df_merged.to_excel(r'C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\data\processed\pro_evasao.xlsx', index=False)

