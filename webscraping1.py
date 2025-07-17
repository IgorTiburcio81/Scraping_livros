#Biliotecas
from bs4 import BeautifulSoup
import requests
import pandas as pd

#Requisição
url = 'https://books.toscrape.com/catalogue/category/books/classics_6/index.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

#Extração e Estruturação dos Dados
star_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5} # mapeando avaliação dos livros
books_data = []
products = soup.find_all('article', class_='product_pod')

# Iteramos sobre cada 'product' e extraímos todos os dados de uma vez
for product in products:
    title = product.find('h3').find('a').get('title')
    # Extrai o texto da classe e usa o dicionário para converter
    star_text = product.find('p', class_='star-rating').get('class')[1]
    stars = star_map.get(star_text, 0)
    # Extrai o preço e já transforma em float
    price = float(product.find('p', class_='price_color').text.strip('£'))
    # Adicionando um dicionário para cada livro na lista
    books_data.append({
        'title': title,
        'stars': stars,
        'price': price
    })

# Criando DataFrame 
df = pd.DataFrame(books_data)

#Ordenando DataFrame
df_ordenado = df.sort_values(by='stars', ascending=False)

#Resultado
print(df_ordenado.head())
df_ordenado.info()

#Salvando em csv
df.to_csv('Scraping_livros.csv')

