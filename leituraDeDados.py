from dotenv import load_dotenv
import os
import serial
import time
import mysql.connector
from datetime import datetime

load_dotenv()
arduino = serial.Serial(os.environ['PORTA_USB'], 9600)
soma_temperatura = 0
soma_umidade = 0
loopings = 0
media_umidade = 0
indice_umidade_problematico = 0.0 

mydb = mysql.connector.connect(
    host=os.environ['DATABASE_HOST'],
    user=os.environ['DATABASE_USER'],
    password=os.environ['DATABASE_PASSWORD'],
    database=os.environ['DATABASE_NAME']
)
cursor = mydb.cursor()

insert_to_database_query = ("INSERT INTO registro_umidade "
               "(umidade, temperatura, data_registro, umidade_problematica) "
               "VALUES (%s, %s, %s, %s)")

def preparaExibicao(leitura_de_dados):
    leitura_de_dados = linha.replace("b'", "").replace("\\r\\n'", "")
    return leitura_de_dados

def organiza_dados(preparacao_dados):
    umidade = preparacao_dados[0].split(':')[1].replace(" ", "")
    temperatura = preparacao_dados[1].split(':')[1].replace(" ", "")
    return [umidade, temperatura]

while True:
    loopings += 1
    linha = str(arduino.readline())
    leitura_de_dados = preparaExibicao(linha)
    print(leitura_de_dados)

    preparacao_dados = leitura_de_dados.split("|")
    umidade_e_temperatura = organiza_dados(preparacao_dados)

    umidade = float(umidade_e_temperatura[0])
    temperatura = float(umidade_e_temperatura[1])

    soma_umidade += umidade
    soma_temperatura += temperatura
    media_umidade = soma_umidade/loopings

    if (umidade >= 12 and umidade <= 20):
        indice_umidade_problematico = umidade
        print("UMIDADE PREOCUPANTE REGISTRADA")

    time.sleep(10)
    if (loopings == 3):
        break

data_atual = datetime.now().date()
dados_umidade = (umidade, temperatura, data_atual, indice_umidade_problematico)
cursor.execute(insert_to_database_query, dados_umidade)

mydb.commit()
cursor.close()
mydb.close()