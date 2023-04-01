import time
import pdfkit
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Pesquisar No Input
searchArg = "Teste de Software"

# Url Que Abre No Browser
byPassUr1 = "http://portal.pucminas.br/biblioteca/index_padrao.php"

options = Options()

# AbrirONavegador
options = webdriver.ChromeOptions()

# Desabilita o PopUp
options.add_argument('--disable-notifications')

# Desabilita o Audio
options.add_argument('--mute-audio')

# Pega os Input
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# Abre a Url
driver.get(byPassUr1)

# Pega o Input
livros_dict = {}

# Pesquisa No Input
searchInput = driver.find_element(By.XPATH, '//*[@id="searchboxholdingsid"]')

# Envia O Input
searchInput.send_keys(searchArg)

# Clica No Botão
driver.find_element(By.XPATH, '//*[@id="searchformholdingsid"]/button').click()

# Espere 30 Segundos
time.sleep(30)

#Fecha Janela de Dialogo
driver.switch_to.alert.accept()

# Troca De Aba
driver.switch_to.window(driver.window_handles[1])

# Clica No Botão
driver.find_element(By.XPATH, '//*[@id="proceed-button"]').click()

# Espera 5 Segundos
time.sleep(25)

# 5 paginas
for j in range(1):
    print('Pagina: ' + str(j+1))
    grupoLivros = driver.find_element(By.CLASS_NAME, 'result-list') 
    listaLivros = grupoLivros.find_elements(By.TAG_NAME, 'li')

    for i in range(1): 
        linkLivro = listaLivros[i].find_element(By.TAG_NAME, 'a')
        link = linkLivro.get_attribute('href')
        livro = {linkLivro.text: link}
        livros_dict.update({i: livro})

    time.sleep(5)  # espera mais 5 segundos antes de ir para a próxima página
    driver.find_element(By.CLASS_NAME, 'next').click()

time.sleep(5)  # espera mais 5 segundos antes de fechar a janela

# Imprime o dicionário com as informações dos livros
print(livros_dict)

# converter dicionário em tabela HTML
table_html = '<table><tr><th>Nome</th><th>Link</th></tr>'
for key, value in livros_dict.items():
    table_html += f'<tr><td>{value[0]}</td><td>{value[1]}</td></tr>'
table_html += '</table>'

# Salva a tabela HTML em um arquivo
pathTohktmltopdf = r'C:\Program Files\\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=pathTohktmltopdf)

for bookPage in livros_dict:
    pdfkit.from_url(livros_dict[bookPage][1], livros_dict[bookPage][0] + '.pdf', configuration=config)

# Gerar PDF
pdfkit.from_string(table_html, 'livros.pdf', configuration=config)

