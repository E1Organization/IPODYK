import aiosqlite


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    async def create_user_table(self, tg_user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.executescript(f'''CREATE TABLE IF NOT EXISTS tg_{tg_user_id} (
                id INTEGER PRIMARY KEY,
                url TEXT,
                user_id INTEGER,
                price REAL
            )''')
            await conn.commit()

    async def table_exists(self):
        async with aiosqlite.connect(self.db_file) as conn:
            sql = await conn.cursor()

            await sql.execute("SELECT name FROM sqlite_master WHERE type='table'")
            name_list = await sql.fetchall()
            return [i[0] for i in name_list]


    async def add_product(self, url, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute(f"INSERT INTO tg_{user_id} (url, user_id, price) VALUES (?, ?, ?)", (url, user_id, 0))
            await conn.commit()
            return cursor.lastrowid

    async def get_user_products(self, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute(f"SELECT * FROM tg_{user_id}")
            rows = await cursor.fetchall()
            await conn.commit()
            return [{'id': row[0], 'url': row[1], 'price': row[3]} for row in rows]

    async def remove_product(self, product_id, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute(f"DELETE FROM tg_{user_id} WHERE id = ? AND user_id = ?", (product_id, user_id))
            await conn.commit()
            return cursor.rowcount > 0
    async def update_price(self, product_id, price, user_id):
        async with aiosqlite.connect(self.db_file) as conn:
            await conn.execute(f"UPDATE tg_{user_id} SET price = ? WHERE id = ?", (price, product_id))
            await conn.commit()


    async def get_all_products(self):
        async with aiosqlite.connect(self.db_file) as conn:
            data = []
            for name_table in await self.table_exists():
                cursor = await conn.execute(f"SELECT * FROM {name_table}")
                rows = await cursor.fetchall()
                await conn.commit()
                data += [{'id': row[0], 'url': row[1], 'user_id': row[2], 'price': row[3]} for row in rows]
            return data

    async def get_all_user_ids(self):
        async with aiosqlite.connect(self.db_file) as conn:
            cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = await cursor.fetchall()
            user_ids = [name[0].replace('tg_', '') for name in tables if name[0].startswith('tg_')]
            return [int(user_id) for user_id in user_ids]
