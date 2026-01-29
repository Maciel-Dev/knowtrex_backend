import re

import bs4
from requests import Session

from models import Product, Products

urls_list = [""]


def parse_products(html_path: str) -> Products:
    """Parse HTML file and extract product information"""
    products = Products()

    with open(html_path, 'r', encoding='utf-8') as e_commerce_html:
        soup = bs4.BeautifulSoup(e_commerce_html.read(), 'html.parser')

    main_slot = soup.find('div', {'class': 's-main-slot'})
    if not main_slot:
        return products

    items = main_slot.find_all('div', {'data-component-type': 's-search-result'})

    for item in items:
        product = Product(
            product_name=_extract_product_name(item),
            product_price=_extract_price(item),
            is_bestseller=_is_bestseller(item),
            rating=_extract_rating(item),
            img_url=_extract_img_url(item)
        )
        products.products.append(product)

    return products


def parse_products_url(url: str) -> Products:
    """Parse HTML file and extract product information"""
    session = Session()
    products = Products()

    get_data = session.get(url)
    data = get_data.json()["data"]
    for product in data:
        product = Product(
            product_name=product["attributes"]["title"],
            product_price=product["attributes"]["price"],
            is_bestseller=False,
            rating=product["attributes"]["score_of_ratings"],
            img_url=product["attributes"]["photos"]["m"][0]
        )
        products.products.append(product)

    return products



def _extract_product_name(item) -> str:
    """Extract and clean product name"""
    element = item.find('a', {'class': 'a-link-normal a-text-normal'})
    return ' '.join(element.text.split()) if element else None


def _extract_price(item) -> float:
    """Extract and convert price to float"""
    whole = item.find('span', {'class': 'a-price-whole'})
    fraction = item.find('span', {'class': 'a-price-fraction'})
    if whole and fraction:
        whole_value = re.sub(r'[^\d]', '', whole.text)
        return float(whole_value + '.' + fraction.text)
    return None


def _is_bestseller(item) -> bool:
    """Check if product is a bestseller"""
    return bool(item.find('span', {'class': 'a-badge-text'}))


def _extract_rating(item) -> float:
    """Extract rating as float"""
    element = item.find('span', {'class': 'a-icon-alt'})
    if element:
        match = re.search(r'[\d,\.]+', element.text)
        if match:
            return float(match.group().replace(',', '.'))
    return None


def _extract_img_url(item) -> str:
    """Extract product image URL"""
    img = item.find('img', {'class': 's-image'})
    return img.get('src') if img else None
