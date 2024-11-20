import aiosqlite


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    async def create_tables(self):
        async with aiosqlite.connect(self.db_file) as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                url TEXT,
                user_id INTEGER,
                price REAL
            )''')
            await conn.commit()

    async def add_product(self, url, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("INSERT INTO products (url, user_id, price) VALUES (?, ?, ?)", (url, user_id, 0))
            await conn.commit()
            return cursor.lastrowid

    async def get_user_products(self, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
            rows = await cursor.fetchall()
            return [{'id': row[0], 'url': row[1], 'price': row[3]} for row in rows]

    async def remove_product(self, product_id, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("DELETE FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
            await conn.commit()
            return cursor.rowcount > 0

    async def update_price(self, product_id, price):
        async with aiosqlite.connect(self.db_file) as conn:
            await conn.execute("UPDATE products SET price = ? WHERE id = ?", (price, product_id))
            await conn.commit()

    async def get_all_products(self):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT * FROM products")
            rows = await cursor.fetchall()
            return [{'id': row[0], 'url': row[1], 'user_id': row[2], 'price': row[3]} for row in rows]
