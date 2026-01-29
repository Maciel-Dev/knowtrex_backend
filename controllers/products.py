from typing import Optional

from starlette.responses import JSONResponse

from services import parse_products
from services.scraper import parse_products_url


def list_products(name: str = "", best_seller: bool = False, min_rating: float = 0):
    """Returns a list with all products in the page"""
    products = parse_products('pages/content.html')

    products.products = [
        p for p in products.products
        if (not best_seller or p.is_bestseller)
           and (not name or name.lower() in p.product_name.lower())
           and (min_rating == 0 or (p.rating is not None and p.rating >= min_rating))
    ]

    return JSONResponse(content=products.to_dict())

def list_products_fixed_url(url: str):
    products = parse_products_url(url)
    return JSONResponse(content=products.to_dict())

def filter_by_rating(
    rating: Optional[float] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None
):
    """Filter products by rating.

    Args:
        rating: Exact rating to filter by
        min_rating: Minimum rating (inclusive)
        max_rating: Maximum rating (inclusive)
    """
    products = parse_products('pages/content.html')

    products.products = [
        p for p in products.products
        if p.rating is not None
           and (rating is None or p.rating == rating)
           and (min_rating is None or p.rating >= min_rating)
           and (max_rating is None or p.rating <= max_rating)
    ]

    return JSONResponse(content=products.to_dict())
