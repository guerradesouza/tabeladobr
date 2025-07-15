import requests
from bs4 import BeautifulSoup

URL = "https://www.espn.com.br/futebol/classificacao/_/liga/BRA.1"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def main():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a tabela principal — ajusta se o layout mudar!
    tabela = soup.find('table')

    if not tabela:
        raise Exception("Tabela não encontrada. Verifique o layout do site.")

    # HTML final com estilos e a tabela extraída
    html_final = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8" />
        <title>Tabela Brasileirão Série A - ESPN</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                background: white;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #003366;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h2>Tabela do Brasileirão Série A - ESPN</h2>
        {str(tabela)}
    </body>
    </html>
    """

    # Salvar arquivo index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_final)

    print("Arquivo index.html gerado com sucesso!")

if __name__ == "__main__":
    main()
