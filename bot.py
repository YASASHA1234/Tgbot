import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')  # Токен будем брать из переменной окружения
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# База товаров (потом можно перенести в БД)
PRODUCTS = {
    'phone': {'name': '📱 iPhone 15', 'price': '89 990₽', 'desc': 'Новый, запечатанный'},
    'laptop': {'name': '💻 MacBook Air', 'price': '94 990₽', 'desc': 'M2, 256GB'},
    'watch': {'name': '⌚ Apple Watch', 'price': '34 990₽', 'desc': 'Series 9, 41mm'},
}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🛍 Каталог", callback_data="catalog"),
        InlineKeyboardButton("🛒 Корзина", callback_data="cart"),
        InlineKeyboardButton("📞 Контакты", callback_data="contacts"),
        InlineKeyboardButton("ℹ️ О магазине", callback_data="about")
    )
    await message.answer(
        "👋 Добро пожаловать в наш магазин!\n\n"
        "Выберите раздел:",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def show_catalog(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    for key, product in PRODUCTS.items():
        kb.add(InlineKeyboardButton(
            f"{product['name']} - {product['price']}", 
            callback_data=f"product_{key}"
        ))
    kb.add(InlineKeyboardButton("◀️ Главное меню", callback_data="main"))
    
    await callback.message.edit_text(
        "📦 Наш каталог товаров:",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith('product_'))
async def show_product(callback: types.CallbackQuery):
    product_key = callback.data.replace('product_', '')
    product = PRODUCTS.get(product_key)
    
    if product:
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("💳 Купить", callback_data=f"buy_{product_key}"),
            InlineKeyboardButton("🛒 В корзину", callback_data=f"add_{product_key}")
        )
        kb.add(InlineKeyboardButton("◀️ Назад", callback_data="catalog"))
        
        await callback.message.edit_text(
            f"**{product['name']}**\n\n"
            f"💰 Цена: {product['price']}\n"
            f"📝 Описание: {product['desc']}",
            parse_mode="Markdown",
            reply_markup=kb
        )

@dp.callback_query_handler(lambda c: c.data == 'main')
async def back_to_main(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🛍 Каталог", callback_data="catalog"),
        InlineKeyboardButton("🛒 Корзина", callback_data="cart"),
        InlineKeyboardButton("📞 Контакты", callback_data="contacts")
    )
    await callback.message.edit_text(
        "👋 Главное меню:",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == 'contacts')
async def show_contacts(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("◀️ Назад", callback_data="main"))
    
    await callback.message.edit_text(
        "📞 Наши контакты:\n\n"
        "📱 Телефон: +7 (999) 123-45-67\n"
        "📧 Email: shop@example.com\n"
        "🕐 Работаем: 10:00 - 22:00",
        reply_markup=kb
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
