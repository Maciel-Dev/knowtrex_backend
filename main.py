from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import list_products as get_products
from controllers import list_products_fixed_url as get_products_url
from controllers.products import filter_by_rating as get_products_by_rating
from controllers.ai_scraper import get_product_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/list_products')
def list_products(name: str = "", best_seller: bool = False, min_rating: float = 0):
    """Returns a list with all products in the page"""
    return get_products(name=name, best_seller=best_seller, min_rating=min_rating)

@app.get('/list_products_url')
def list_products_url(url=r""):
    return get_products_url(url)

@app.get('/search_ai')
async def search_ai(url: str = "", description: str = ""):
    """Search for products using AI-powered search"""
    return await get_product_ai(url=url, description=description)


@app.get('/products/filter_by_rating')
def products_by_rating(
    rating: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None
):
    """Filter products by rating.

    - rating: Filter by exact rating value
    - min_rating: Filter by minimum rating (inclusive)
    - max_rating: Filter by maximum rating (inclusive)
    """
    return get_products_by_rating(rating=rating, min_rating=min_rating, max_rating=max_rating)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)