import random
from data.database import Database
db = Database("data/products.db")

class PriceTracker:
    def __init__(self):
        pass

    async def check_prices(self, user_id):
        products = await db.get_all_products()
        changes = []
        for product in products:
            new_price = random.randint(900, 1100)
            if new_price is not None and new_price != product['price']:
                change_percent = (
                    round(((new_price - product['price']) / product['price']) * 100, 2) 
                    if product['price'] else 0
                )
                changes.append({
                    'user_id': product['user_id'],
                    'url': product['url'],
                    'old_price': product['price'],
                    'new_price': new_price,
                    'change_percent': change_percent
                })
                await db.update_price(product['id'], new_price, user_id)
        return changes

    # def get_price(self, url):
    #     # Заглушка для парсинга цен. Замените это на настоящий парсер.
    #     return random.randint(900, 1100)
