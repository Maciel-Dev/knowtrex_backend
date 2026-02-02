from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controllers import list_products as get_products
from controllers.products import filter_by_rating as get_by_rating, list_products_fixed_url
from controllers.ai_scraper import get_product_ai
from helper.disposable_urls import get_categories, build_category_url, get_category_slugs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/products')
def get_all_products():
    """Returns all products"""
    return get_products()


@app.get('/products/search')
def search_products(name: str):
    """Search products by name"""
    return get_products(name=name)


@app.get('/products/bestsellers')
def get_bestsellers():
    """Returns only bestseller products"""
    return get_products(best_seller=True)


@app.get('/products/by-rating')
def filter_products_by_rating(
    rating: float = None,
    min_rating: float = None,
    max_rating: float = None
):
    """Filter products by rating criteria"""
    return get_by_rating(rating=rating, min_rating=min_rating, max_rating=max_rating)


# Available category slugs for filtering
# "Amazon" uses None to indicate it calls the /products endpoint
PRODUCT_CATEGORIES = {
    "Amazon": None,
    "Hardware": "hardware",
    "Periféricos": "perifericos",
    "Gamer": "gamer",
    "Smartphone": "celular-smartphone",
    "Tv": "tv",
    "Audio": "audio",
    "Projectors": "projetores",
    "Office": "escritorio",
    "Smart House": "casa-inteligente"
}


@app.get('/products/categories')
def get_product_categories():
    """Returns list of category names for filtering"""
    return {
        "categories": list(PRODUCT_CATEGORIES.keys())
    }


@app.get('/products/by-category')
def filter_products_by_category(category: str, page: int = 1, size: int = 20):
    """Get products filtered by category name"""
    if category not in PRODUCT_CATEGORIES:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")

    slug = PRODUCT_CATEGORIES.get(category)

    # Amazon category returns products from /products endpoint
    if slug is None:
        return get_products()

    url = build_category_url(slug, page=page, size=size)
    return list_products_fixed_url(url)


@app.get('/search_ai')
async def search_ai(url: str = "", description: str = ""):
    """Search for products using AI-powered search"""
    return await get_product_ai(url=url, description=description)


@app.get('/categories')
def list_categories():
    """Returns all available categories from Kabum API"""
    categories = get_categories()
    return {
        "total": len(categories),
        "categories": [
            {"slug": cat["amigavel"], "name": cat["nome"], "id": cat["codigo"]}
            for cat in categories
        ]
    }


@app.get('/categories/{slug}/products')
def get_products_by_category(slug: str, page: int = 1, size: int = 20):
    """Get products from a specific category by its slug (amigavel)"""
    valid_slugs = get_category_slugs()
    if slug not in valid_slugs:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")

    url = build_category_url(slug, page=page, size=size)
    return list_products_fixed_url(url)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)