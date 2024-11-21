import requests
import re
from pathlib import Path
import json
from funcoes import check_case, filter_case_1, filter_case_2, generate_links, alteracoes_tecnicas, gerar_despachos_html, aplicar_BeautifulSoup, filtrar_despacho_individual, gerar_texto_final
from bs4 import BeautifulSoup
import datetime

hoje = datetime.date.today()
dia_link_pdf_individual = hoje.strftime("%d")
mes_link_pdf_individual = hoje.strftime("%m")
ano_link_pdf_individual = hoje.year

url_hoje = "https://www.in.gov.br/leiturajornal?org=Minist%C3%A9rio%20de%20Minas%20e%20Energia&org_sub=Ag%C3%AAncia%20Nacional%20de%20Energia%20El%C3%A9trica&ato=Despacho"

data_escolha = input("Deseja usar o diário de hoje? (s/n) ")
if data_escolha == 's':
    url_escolhido = url_hoje
    dia_escolhido = dia_link_pdf_individual
    mes_escolhido = mes_link_pdf_individual
    ano_escolhido = ano_link_pdf_individual
else:
    data_desejada = input("Digite a data desejada: (dd-mm-aaaa) ")
    dia_escolhido, mes_escolhido, ano_escolhido = map(
        int, data_desejada.split('-'))
    url_escolhido = f"https://www.in.gov.br/leiturajornal?data={dia_escolhido}-{mes_escolhido}-{ano_escolhido}&org=Minist%C3%A9rio%20de%20Minas%20e%20Energia&org_sub=Ag%C3%AAncia%20Nacional%20de%20Energia%20El%C3%A9trica&ato=Despacho#daypicker"


response = requests.get(url_escolhido, timeout=100)

with open('Response.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)

with open('Response.txt', 'r', encoding='utf-8') as file:
    dou = file.read()

matches = re.findall(r'\{"pubName":(?:.|\s)*?\}', dou, re.DOTALL)
matches = [json.loads(match) for match in matches]
# print(json.dumps(matches, indent=4))

case = check_case(matches)
print(case)

if case == 'case 1':
    resultado = filter_case_1(matches)
elif case == 'case 2':
    resultado = filter_case_2(matches)

resultado_alteracoes = alteracoes_tecnicas(matches)


'''for key, value in resultado[0].items():
    print(f"{key}:{value}")'''

try:
    page_num = int(resultado[0]['numberPage'])
    print(f"Página do DOU = {page_num}")
    url_pagina_geracao_pdf = f"Link para páginado do DOU (Geração): https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?jornal=515&pagina={page_num}&data={dia_escolhido}/{mes_escolhido}/{ano_escolhido}"
except IndexError:
    print("Não há despachos de geração hoje")
    url_pagina_geracao_pdf = ''

try:
    page_num_alteracoes_tecnicas = page_num = int(
        resultado_alteracoes[0]['numberPage'])
    print(f"Página do DOU = {page_num_alteracoes_tecnicas}")
    url_pagina_alteracoes_pdf = f"Link para páginado do DOU (Alterações técnicas): https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?jornal=515&pagina={page_num_alteracoes_tecnicas}&data={dia_escolhido}/{mes_escolhido}/{ano_escolhido} "
except IndexError:
    print("Não há alterações técnicas hoje")
    url_pagina_alteracoes_pdf = ''


links = generate_links(resultado)

link_alteracoes = generate_links(resultado_alteracoes)


print(f"há {len(links)} links")

print(f"há {len(resultado)} dicionários")
print(f"há {len(resultado_alteracoes)} dicionários de alteracao")

# colocar os resultados de get de cada link em uma nova lista (despachos_html)

despachos_html = gerar_despachos_html(links)
despachos_html_alteracoes = gerar_despachos_html(link_alteracoes)
# print(f"há {len(despachos_html)} despachos_html")

# aplicar beautifulsoup em cada um dos arquivos htmls da lista despachos_html
despacho_individual_html = aplicar_BeautifulSoup(despachos_html)
despacho_individual_html_alteracoes = aplicar_BeautifulSoup(
    despachos_html_alteracoes)
# print(f"há {len(despacho_individual_html)} despachos_individual_html")

# alocar apenas os textos das tags <p class="dou-paragraph"> em cada despacho
despacho_individual_filtrado = filtrar_despacho_individual(
    despacho_individual_html)
despacho_individual_filtrado_alteracoes = filtrar_despacho_individual(
    despacho_individual_html_alteracoes)
# print(f"há {len(despacho_individual_filtrado)} despacho_individual_filtrado")

# tirar as tags do texto
despacho_individual_texto = []
texto_completo = ''
for i in range(len(despacho_individual_filtrado)):
    # Iterar sobre cada tag <p> encontrada e extrair o texto
    # Junta todos os textos de <p>
    texto_completo += despacho_individual_html[i].find(
        'p', class_="identifica").text.rstrip() + '\n\n'
    texto_completo += '\n\n'.join(
        [p.text for p in despacho_individual_filtrado[i]])
    texto_completo += '\n\n\n'
    despacho_individual_texto.append(texto_completo)
    texto_completo = ''

despacho_individual_alteracoes_texto = []
texto_alteracoes_completo = ''
for i in range(len(despacho_individual_filtrado_alteracoes)):
    # Iterar sobre cada tag <p> encontrada e extrair o texto
    # Junta todos os textos de <p>
    texto_alteracoes_completo += despacho_individual_html_alteracoes[i].find(
        'p', class_="identifica").text.rstrip() + '\n\n'
    texto_alteracoes_completo += '\n\n'.join(
        [p.text for p in despacho_individual_filtrado_alteracoes[i]])
    texto_alteracoes_completo += '\n\n\n'
    despacho_individual_alteracoes_texto.append(texto_alteracoes_completo)
    texto_alteracoes_completo = ''

# print(f"há {len(despacho_individual_texto)} despacho_individual_texto")
texto = ''
texto_final = gerar_texto_final(texto, despacho_individual_texto)

texto1 = ''
texto_final_alteracoes = gerar_texto_final(
    texto1, despacho_individual_alteracoes_texto)

'''for elemento in despacho_individual_texto:
    texto_final += elemento'''


# adicionar link página pdf
texto_combinado = texto_final+texto_final_alteracoes
texto_combinado += url_pagina_geracao_pdf + '\n\n' + url_pagina_alteracoes_pdf
print(texto_combinado)
