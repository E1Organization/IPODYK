import requests

async def GET_PRICE(CODE):
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://global.wildberries.ru',
        'priority': 'u=1, i',
        'referer': 'https://global.wildberries.ru/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-captcha-id': 'Catalog 1|1|1734527683|AA==|b8c1c72de41d4ad5a1a53330788f9e3d|SbhR20u4fLcXw5Igx4soqUMmVZz41z1qmP6Y8vgyZyC',
    }

    url = f'https://card.wb.ru/cards/v2/detail?nm={CODE}&appType=128&curr=byn&lang=ru&dest=-1257786&spp=30'

    # Выполните запрос
    response = requests.get(url, headers=headers)

    # Проверьте статус ответа
    if response.status_code == 200:
        data = response.json()  # Получите JSON-ответ
        products = data.get('data', {}).get('products', [])

        for product in products:
            price = product.get('sizes', [{}])[0].get('price', {}).get('total')  # Цена товара
            if price is not None:
                return price / 100.0  # Возвращаем точную цену в рублях с копейками

    # Если запрос не удался
    print(f"Error fetching price, status code: {response.status_code}")
    return None
