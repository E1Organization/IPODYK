import random


class PriceTracker:
    def __init__(self, db):
        self.db = db

    async def check_prices(self):
        products = await self.db.get_all_products()
        changes = []
        for product in products:
            new_price = self.get_price(product['url'])
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
                await self.db.update_price(product['id'], new_price)
        return changes

    def get_price(self, url):
        # Заглушка для парсинга цен. Замените это на настоящий парсер.
        return random.randint(900, 1100)
