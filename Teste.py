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
time.sleep(15)

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

driver.find_element(By.CLASS_NAME, 'next').click()

# converter dicionário em tabela HTML
table_html = '<table><tr><th>Nome</th><th>Link</th></tr>'
for key, value in livros_dict.items():
    table_html += f'<tr><td>{key}</td><td><a href="{value}">{value}</a></td></tr>'
table_html += '</table>'

# Salvar a tabela HTML em um arquivo
with open('livros.html', 'w', encoding='utf-8') as f:
    f.write(table_html)

# Diretório de saída do PDF
pdf_directory = os.path.join(os.getcwd(), 'pdfs')

# Verificar se o diretório existe, se não, criá-lo
if not os.path.exists(pdf_directory):
    os.mkdir(pdf_directory)

# Gerar o arquivo PDF a partir do arquivo HTML
pdf_path = os.path.join(pdf_directory, 'livros.pdf')
pdfkit.from_file('livros.html', pdf_path)

# Exibir o caminho absoluto do arquivo PDF
print(f"Arquivo PDF gerado em: {pdf_path}")