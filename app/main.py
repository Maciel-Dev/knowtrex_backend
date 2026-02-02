# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from controllers import list_products as get_products
# from controllers.ai_scraper import get_product_ai
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# @app.get('/list_products')
# def list_products(name: str = "", best_seller: bool = False, min_rating: float = 0):
#     """Returns a list with all products in the page"""
#     return get_products(name=name, best_seller=best_seller, min_rating=min_rating)
#
# @app.get('/search_ai')
# async def search_ai(url: str = "", description: str = ""):
#     """Search for products using AI-powered search"""
#     return await get_product_ai(url=url, description=description)
