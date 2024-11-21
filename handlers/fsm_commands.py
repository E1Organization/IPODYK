from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from data.database import Database
from handlers.price_tracker import PriceTracker
from keyboards.reply import main_menu, rmk
from keyboards.builders import generator
from utils.states import Add, Remove

router = Router()
pt = PriceTracker()
db = Database("data/products.db")

#отмена
@router.message(F.text == "❌ Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=main_menu)


#добавление товара
@router.message(F.text.lower() == "🖥️ добавить товар")
async def add_product(message: Message, state: FSMContext):
    await state.set_state(Add.link)
    await message.answer("Отправьте ссылку на товар:",
                         reply_markup=generator("❌ Отмена"))

@router.message(Add.link, F.text)
async def link_product(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    await state.clear()

    #добавить валидатор ссылки

    product_id = await db.add_product(data["link"], message.from_user.id)
    if product_id:
        await message.reply(f"✅ Товар добавлен для отслеживания. ID: {hbold(product_id)}",
                            reply_markup=main_menu)
    else:
        await message.reply("❌ Не удалось добавить товар. Проверьте ссылку и попробуйте снова.")

@router.message(Add.link, ~F.text)
async def inc_link_product(message: Message, state: FSMContext):
    await message.answer("❌ Не удалось добавить товар. Проверьте ссылку и попробуйте снова.",
                         reply_markup=generator("❌ Отмена"))


#удаление товара
@router.message(F.text.lower() == "✂️ удалить товар")
async def rem_product(message: Message, state: FSMContext):
    await state.set_state(Remove.id)
    await message.answer("Отправьте ID товарa:",
                         reply_markup=generator("❌ Отмена"))

@router.message(Remove.id, F.text)
async def id_rem_product(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    await state.clear()

    if await db.remove_product(data["id"], message.chat.id):
        await message.reply(f"✅ Товар с ID {hbold(data["id"])} удален из отслеживания.")
    else:
        await message.reply("❌ Не удалось удалить товар. Проверьте ID и попробуйте снова.")

@router.message(Remove.id, ~F.text)
async def inc_id_rem_product(message: Message, state: FSMContext):
    await message.answer("❌ Не удалось удалить товар. Проверьте ID и попробуйте снова.",
                         reply_markup=generator("❌ Отмена"))
    

#лист товаров
@router.message(F.text.lower() == "🗒️ просмотреть отслеживаемые товары")
async def add_product(message: Message):
    products = await db.get_user_products(message.from_user.id)
    if not products:
        await message.reply("📋 Ваш список отслеживаемых товаров пуст.")
    else:
        response = "📋 Ваши отслеживаемые товары:\n"
        for p in products:
            response += f"ID: {hbold(p['id'])}, URL: {p['url']}, Текущая цена: {hbold(p['price'])} ₽\n"
        await message.reply(response)

