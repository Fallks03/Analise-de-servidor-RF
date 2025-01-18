# Inicio

import requests, bs4, csv, time, os
from datetime import datetime
from bs4 import BeautifulSoup

print('Codigo Iniciado')
while True:
    horaAtual = datetime.now().strftime("%d/%m/%Y %H:%M") #pega a hora que o loop foi feito
    print('.')
    servidorComFalha = False #indentifica se possui um problema nos status dos serviços

    try:
        #puxa o conteudo da pagina
        content = requests.get('http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=P2c98tUpxrI=').text
    except:
        print(horaAtual, "> Erro ao acessar servidor")
        time.sleep(300)
        continue #reinicia o loop

    soup = BeautifulSoup(content, 'html.parser')

    #puxa a matriz do site e salva em um objeto
    tableHtml = soup.find('table', class_='tabelaListagemDados')

    #salva todas linhas em um objeto list
    linha = tableHtml.find_all('tr')

    matriz = [] #salva toda matriz html formatada em uma list de list [][]

    for i in range(len(linha)):
        if linha[i].find_all('td'):
            matriz.append(linha[i].find_all('td')) 
        else:
            matriz.append(linha[i].find_all('th'))
            #adiciona no objeto matriz uma lista de colunas(<td> ou <th>) da linha[i]

    #troca os as tag <td> de bola de status por numero de 0 a 2
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            conteudo = str(matriz[i][j])
            if conteudo == '<td><img src="imagens/bola_verde_P.png"/></td>':
                matriz[i][j] = 2
            elif conteudo == '<td><img src="bola_amarela_G.png"/></td>':
                matriz[i][j] = 1
            elif conteudo == '<td><img src="bola_vermelho_G.png"/></td>':
                matriz[i][j] = 0
            else:
                #extrai o texto de celulas que não são bolas de status
                matriz[i][j] = matriz[i][j].get_text() 

    #a tabela armazenará a matriz filtrada
    tabela = []

    #filtra apenas as colunas desejadas e salva no objeto matriz
    for i in range(len(matriz)):
        novaLinha = []
        for j in range(len(matriz[i])):
            # Verificar se a celula esta dentro de uma coluna desejada
            if matriz[0][j] in ["Autorizador", "Autorização4", "Status Serviço4"]:
                celulaAtual = matriz[i][j]
                novaLinha.append(celulaAtual)
                #verifica se a celula atual possui algum problema, se sim, printa um alarme
                if type(celulaAtual) == int: 
                    if celulaAtual < 2:
                        servidorComFalha = True
                        print(
                            horaAtual, ">", matriz[i][0], matriz[0][j] + ":", 
                            "operando com falha" if celulaAtual == 1 else "Indisponível"
                        )
        tabela.append(novaLinha)

    csvSalvo = []
    try:
        with open("Desafio-PinPoint/status_servicos.csv", mode="r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for linha in reader:
                csvSalvo.append(linha)
    except:
        with open("status_servicos.csv", mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerows(tabela)

    if csvSalvo != tabela:
        horaAtual = datetime.now().strftime("%d.%m.%Y_%H-%M")
        status = 'Erro' if servidorComFalha else 'Normal'
        with open('Historico/status_' + horaAtual + '_' + status,
                mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerows(tabela)

    time.sleep(300)










