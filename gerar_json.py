from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import traceback

# Configura navegador (visual para debug)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    url = "https://www.ogol.com.br/competicao/brasileirao"
    driver.get(url)

    # Aguarda carregar o wrapper da tabela de classificação
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "DataTables_Table_0_wrapper"))
    )

    # Scroll para garantir carregamento de todos os elementos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Extrai a tabela específica via BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tabela_html = soup.find("table", {"id": "DataTables_Table_0"})

    if tabela_html:
        df = pd.read_html(str(tabela_html))[0]

        # Exibe para debug
        print(df.head())

        # Salva em JSON
        df.to_json("tabela.json", orient="records", force_ascii=False, indent=2)
        print("✅ Tabela de classificação salva como tabela.json!")
    else:
        print("❌ Tabela de classificação não encontrada.")

except Exception as e:
    print("❌ Erro ao extrair a tabela:")
    traceback.print_exc()

finally:
    driver.quit()
