# %%
import tabula
import pandas as pd
import os
from datetime import date, timedelta

# Seu código para ler o PDF e extrair as tabelas de todas as páginas
directory = "/home/oem/Documentos/frontend-basico/ze/"
file_path = "/home/oem/Documentos/frontend-basico/ze/historico_de_entregas_1.pdf"
tabelas = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
if not os.path.exists(directory):
    os.makedirs(directory)
valores_quarta_coluna = []
# Itera sobre as tabelas e pega os valores da quarta coluna de cada uma
for i, tabela_atual in enumerate(tabelas, start=1):
    # Pega os valores da quarta coluna
    quarta_coluna = tabela_atual.iloc[:, 3].tolist()
    valores_quarta_coluna.extend(quarta_coluna)
# Se encontrou algum valor, cria um DataFrame com esses valores
if valores_quarta_coluna:
    df_resultado = pd.DataFrame({"Quarta Coluna": valores_quarta_coluna})
    # Nome do arquivo Excel
    nome_arquivo_excel = "planilha_quarta_coluna.xlsx"
    # Caminho completo para o arquivo Excel de saída
    caminho_arquivo_excel = f"{directory}{nome_arquivo_excel}"
    # Salva o DataFrame resultante no arquivo Excel
    df_resultado.to_excel(caminho_arquivo_excel, index=False)    
    print(f"\nValores da quarta coluna de todas as tabelas foram salvos em {caminho_arquivo_excel}")
else:
    print("Não foram encontradas tabelas no PDF.")

# %% [markdown]
# gerando database

# %%
#contar o numero de teles
numero_de_linhas = len(valores_quarta_coluna)
print(f"Ja fez:{numero_de_linhas} teles.")
print(f"Ja fez: R${numero_de_linhas*7} Reais.")



# %% [markdown]
# # Cria um novo DataFrame com as colunas de ano, mês, dia, hora, minuto e segundo
# 

# %%
data_hora_obj = pd.to_datetime(valores_quarta_coluna, format='%Y-%m-%d %H:%M:%S.%f %Z')

# Cria um novo DataFrame com as colunas de ano, mês, dia, hora, minuto e segundo
df_novo = pd.DataFrame({
    'Ano': data_hora_obj.year,
    'Mês': data_hora_obj.month,
    'Dia': data_hora_obj.day,
    'Hora': data_hora_obj.hour,
    'Minuto': data_hora_obj.minute,
    'Segundo': data_hora_obj.second
})

# Exibe o novo DataFrame
print(df_novo)

# %% [markdown]
# #Calcular semana

# %%
# Função para enumerar semanas
def enumerar_semanas(ano):
    data_inicio = date(ano, 1, 1)

    while data_inicio.weekday() != 0:  # 0 representa segunda-feira
        data_inicio += timedelta(days=1)

    numero_semana = 1
    semanas = {}

    while data_inicio.year == ano:
        data_fim = data_inicio + timedelta(days=6)
        semanas[numero_semana] = (data_inicio, data_fim)
        data_inicio += timedelta(days=7)
        numero_semana += 1

    return semanas

# Aplicando a lógica para criar a coluna 'Semanas'
def encontrar_semana(row):
    ano = row['Ano']
    mes = row['Mês']
    dia = row['Dia']
    
    semanas = enumerar_semanas(ano)
    
    for numero_semana, (inicio, fim) in semanas.items():
        if ano == inicio.year and mes == inicio.month:
            if inicio.day <= dia <= fim.day:
                return numero_semana
    
    return None

# Adicionando a coluna 'Semanas' ao DataFrame
df_novo['Semanas'] = df_novo.apply(encontrar_semana, axis=1)

# Exibindo o DataFrame resultante
print(df_novo)

# %% [markdown]
# Trabalhando com as semanas
# Enumerando quantas teles foi feita em cada semana

# %%
def contar_ocorrencias_todas_semanas(dataframe):
    contagem_por_semana = dataframe['Semanas'].value_counts().reset_index()
    contagem_por_semana.columns = ['Número da Semana', 'Ocorrências']
    return contagem_por_semana

# Exemplo de uso
contagem_todas_semanas = contar_ocorrencias_todas_semanas(df_novo)

print("Contagem de ocorrências por semana:")
print(contagem_todas_semanas)


# %% [markdown]
# #Trabalando com o ano

# %%
def contar_ocorrencias_todos_anos(dataframe):
    contagem_por_ano = dataframe['Ano'].value_counts().reset_index()
    contagem_por_ano.columns = ['Ano', 'Ocorrências']
    contagem_por_ano = contagem_por_ano.sort_values(by='Ano')
    return contagem_por_ano

# Exemplo de uso
contagem_todos_anos = contar_ocorrencias_todos_anos(df_novo)

print("Contagem de ocorrências por ano:")
print(contagem_todos_anos)

# %% [markdown]
# #Trabalando com o mes

# %%
def contar_ocorrencias_todos_meses(dataframe):
    contagem_por_mes = dataframe.groupby(['Ano', 'Mês']).size().reset_index(name='Ocorrências')
    contagem_por_mes = contagem_por_mes.sort_values(by=['Ano', 'Mês'])
    return contagem_por_mes

# Exemplo de uso
contagem_todos_meses = contar_ocorrencias_todos_meses(df_novo)

print("Contagem de ocorrências por ano e mês:")
print(contagem_todos_meses)


# #Trabalhando com o Dia

def contar_ocorrencias_todos_dias(dataframe):
    contagem_por_dia = dataframe.groupby(['Ano', 'Mês', 'Dia']).size().reset_index(name='Ocorrências')
    contagem_por_dia = contagem_por_dia.sort_values(by=['Ano', 'Mês', 'Dia'])
    return contagem_por_dia

# Exemplo de uso
contagem_todos_dias = contar_ocorrencias_todos_dias(df_novo)

print("Contagem de ocorrências por ano, mês e dia:")
print(contagem_todos_dias)
