from datetime import date
from datetime import date, timedelta
#função de enumerar semana
def enumerar_semanas(ano):
    data_inicio = date(ano, 1, 1)

    # Encontrar o primeiro dia da primeira semana
    while data_inicio.weekday() != 0:  # 0 representa segunda-feira
        data_inicio += timedelta(days=1)

    numero_semana = 1
    semanas = {}

    while data_inicio.year == ano:
        data_fim = data_inicio + timedelta(days=6)  # Último dia da semana
        semanas[numero_semana] = (data_inicio, data_fim)
        data_inicio += timedelta(days=7)  # Avançar para a próxima semana
        numero_semana += 1

    return semanas
#separa a string data_teste em um array ['2023-11-26', '16:59:04.660', 'America/Sao_Paulo']
data_teste = "2023-11-26 16:59:04.660 America/Sao_Paulo"
data_atual = data_teste.split()
print(data_atual[0])
#Cria uma variavel para ano, mes e dia e pega o array e salva cada variavel
ano, mes, dia = map(int, data_atual[0].split('-'))
nova_data_array = [ano, mes, dia]
print(nova_data_array)
#Encontra a semana certa
semanas = enumerar_semanas(ano)
for numero_semana, (inicio, fim) in semanas.items():
    if ano == inicio.year and mes == inicio.month:
        if inicio.day <= dia <= fim.day:
            print(f"Dentro da semana {numero_semana}, no dia {dia}")