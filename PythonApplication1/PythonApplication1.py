
from bs4 import BeautifulSoup
import requests
import pandas as pd

url_list = [
    "https://bonna.com.tr/urun-kategori/terra-raw/",
    "https://bonna.com.tr/urun-kategori/vega/"
]

data = []
collection = ""  # Initialize the collection variable
for url in url_list:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        product_tags = soup.find_all("span", class_="entry-title")

        for tag in product_tags:
            div_tag = tag.find_previous("div", class_="uvc-main-heading ult-responsive")
            if div_tag:
                h1_tag = div_tag.find("h1")
                if h1_tag:
                    collection = h1_tag.text.strip()  # Update the collection title

            product_name = tag.a.text.strip()
            sku_tag = tag.find_next("div", class_="sku")
            sku = sku_tag.text.strip() if sku_tag else ""
            image_div = tag.find_next("div", class_="woo-buttons-on-img")
            image_tag = image_div.find("img") if image_div else None
            image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else ""
            link = tag.a["href"]

            data.append({
                "Koleksiyon Baþlýðý": collection,
                "Ürün Ýsmi": product_name,
                "SKU": sku,
                "Görsel Linki": image_url,
                "Ürün Linki": link
            })

df = pd.DataFrame(data)

# Add the 'Koleksiyon Stili' column
df["Koleksiyon Stili"] = "--font-weight:theme;margin-bottom:20px;"

# Save the DataFrame to an Excel file
df.to_excel("urunler2.xlsx", index=False)