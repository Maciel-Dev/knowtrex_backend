class Product:
    def __init__(self, product_name, product_price, is_bestseller, rating, img_url):
        self.product_name = product_name
        self.product_price = product_price
        self.is_bestseller = is_bestseller
        self.rating = rating
        self.img_url = img_url

    def to_dict(self):
        return self.__dict__

class Products:
    def __init__(self):
        self.products = []

    def to_dict(self):
        return {"products": [p.to_dict() for p in self.products]}