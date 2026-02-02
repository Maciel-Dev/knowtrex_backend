import httpx

CATEGORIES_API = "https://servicespub.prod.api.aws.grupokabum.com.br/categoria/v1/categoria?ativo=1"
BASE_PRODUCT_URL = "https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/{amigavel}?page_number={page}&page_size={size}&facet_filters=&sort=most_searched&is_prime=false&payload_data=products_category_filters&include=gift"


def get_categories():
    """Fetch all categories from the API"""
    response = httpx.get(CATEGORIES_API)
    response.raise_for_status()
    data = response.json()
    return data.get("categorias", [])


def get_category_slugs():
    """Returns a list of all 'amigavel' slugs"""
    categories = get_categories()
    return [cat["amigavel"] for cat in categories]


def build_category_url(amigavel: str, page: int = 1, size: int = 20):
    """Build a product URL for a given category slug"""
    return BASE_PRODUCT_URL.format(amigavel=amigavel, page=page, size=size)


def get_urls():
    """Returns URLs for all active categories"""
    slugs = get_category_slugs()
    return [build_category_url(slug) for slug in slugs]