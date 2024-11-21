import requests
from bs4 import BeautifulSoup


def check_case(lista):
    case1 = 0
    case2 = 0
    for block in lista:
        if block.get('hierarchyStr') == "Ministério de Minas e Energia/Agência Nacional de Energia Elétrica/Superintendência de Fiscalização Técnica dos Serviços de Energia Elétrica/Gerência de Fiscalização da Geração":
            case1 += 1
        else:
            case2 += 1
    if case1 > 0:
        return ("case 1")
    else:
        return ("case 2")


def alteracoes_tecnicas(lista):
    filtered_blocks = []
    for block in lista:
        if block.get('hierarchyStr') == "Ministério de Minas e Energia/Agência Nacional de Energia Elétrica/Superintendência de Concessões,  Permissões e Autorizações dos Serviços de Energia Elétrica":
            filtered_blocks.append(block)
    return (filtered_blocks)


def filter_case_1(lista):
    filtered_blocks = []
    for block in lista:
        if block.get('hierarchyStr') == "Ministério de Minas e Energia/Agência Nacional de Energia Elétrica/Superintendência de Fiscalização Técnica dos Serviços de Energia Elétrica/Gerência de Fiscalização da Geração":
            filtered_blocks.append(block)
    return (filtered_blocks)


def filter_case_2(lista):
    filtered_blocks = []
    for block in lista:
        if block.get('hierarchyStr') == "Ministério de Minas e Energia/Agência Nacional de Energia Elétrica/Superintendência de Fiscalização Técnica dos Serviços de Energia Elétrica":
            filtered_blocks.append(block)
    return (filtered_blocks)


def generate_links(lista):
    links = []
    for link in lista:
        links.append(f"https://www.in.gov.br/web/dou/-/{link['urlTitle']}")
    return links


def gerar_despachos_html(links):
    despachos_html = []
    for i in range(len(links)):
        despachos_html.append(requests.get(links[i], timeout=100))
    return despachos_html


def aplicar_BeautifulSoup(despachos_html):
    despacho_individual_html = []
    for i in range(len(despachos_html)):
        despacho_individual_html.append(BeautifulSoup(
            despachos_html[i].text, 'html.parser'))
    return despacho_individual_html


def filtrar_despacho_individual(despacho_individual_html):
    despacho_individual_filtrado = []
    for i in range(len(despacho_individual_html)):
        despacho_individual_filtrado.append(
            despacho_individual_html[i].find_all('p', class_="dou-paragraph"))
    return despacho_individual_filtrado


def gerar_texto_final(texto_final, despacho_individual_texto):
    texto_final = ''
    for elemento in despacho_individual_texto:
        texto_final += elemento
    return texto_final
