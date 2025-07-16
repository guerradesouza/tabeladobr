from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import traceback

# Configura navegador em modo visível (pode ajudar a debug)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Removido para debug visual
driver = webdriver.Chrome(options=options)

try:
    url = "https://www.ogol.com.br/competicao/brasileirao"
    driver.get(url)

    # Aguarda o wrapper da tabela (div externa)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "DataTables_Table_0_wrapper"))
    )

    # Força scroll até o fim para carregar a tabela (caso AJAX/lazy loading)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # espera extra para garantir carregamento

    # Agora sim tenta buscar a tabela
    tabela = driver.find_element(By.ID, "DataTables_Table_0")

    # Salva a página para debug
    with open("pagina_completa.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Extrai usando pandas
    tabelas = pd.read_html(driver.page_source)
    print(f"✅ {len(tabelas)} tabelas encontradas!")
    df = tabelas[0]
    print(df.head())

    ## Salvar o DataFrame como JSON
    df.to_json("tabela.json", orient="records", force_ascii=False, indent=2)
    print("✅ Arquivo 'tabela.json' gerado com sucesso!")



except Exception as e:
    print("❌ Erro ao extrair a tabela:")
    traceback.print_exc()
finally:
    driver.quit()
