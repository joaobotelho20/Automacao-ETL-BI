import pandas as pd

def padronizar_datas(df, coluna='Data'):
    """
    Padroniza a coluna de data de um DataFrame para o tipo datetime64[ns].

    Args:
        df (pd.DataFrame): DataFrame com a coluna de data.
        coluna (str): Nome da coluna que contém a data.

    Returns:
        pd.DataFrame: DataFrame com a coluna convertida para datetime.
    """

    # Pular se já for datetime64
    if pd.api.types.is_datetime64_any_dtype(df[coluna]):
        print(f"Coluna '{coluna}': Já está no formato datetime64, mantido como está.")
        return df

    try:
        # Verificar o tipo de separador mais comum
        if df[coluna].dropna().str.contains('/', regex=False).all():
            print(f"Coluna '{coluna}': Convertendo datas com '/'")
            df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce')
        elif df[coluna].dropna().str.contains('-', regex=False).all():
            print(f"Coluna '{coluna}': Convertendo datas com '-' (formato ISO)")
            df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
        else:
            print(f"Coluna '{coluna}': Padrão misto, tentativa geral de conversão")
            df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce')

        num_nulos = df[coluna].isna().sum()
        if num_nulos > 0:
            print(f"Atenção: {num_nulos} valores não puderam ser convertidos em '{coluna}'")
    except Exception as e:
        print(f"Erro ao converter a coluna '{coluna}': {e}")
    
    return df

def normalizar_texto(texto):
    import re
    import unicodedata
    if pd.isna(texto):
        return texto
    # Transforma em string, caixa baixa
    texto = str(texto).lower()
    # Remove acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    # Remove espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

df_list = ['evasao_mes_atual']

for df_name in df_list:

    df = pd.read_excel(fr"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\Raw Data\{df_name}.xls",)
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

    df.to_excel(fr"C:\Users\USER\Desktop\GitHub\Automacao-ETL-BI\Processed Data\{df_name}.xlsx", index=False)