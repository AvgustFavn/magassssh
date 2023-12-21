import asyncio
import logging

from aiogram.utils import executor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ApplicationBuilder, \
    MessageHandler, filters
from back import *

loop = asyncio.get_event_loop()
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    result = await loop.run_in_executor(None, get_user, user)
    if not result:
        keyboard = [
            [InlineKeyboardButton("Посмотреть товары", callback_data='1')],
             [InlineKeyboardButton("Корзина", callback_data='2')],
            [InlineKeyboardButton("Избранное", callback_data='3')],
            [InlineKeyboardButton("Заказы", callback_data='4')],
            [InlineKeyboardButton("Поиск по названию", callback_data='9')],
            [InlineKeyboardButton("Наши контакты", callback_data='11')]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Посмотреть товары", callback_data='1')],
            [InlineKeyboardButton("Корзина", callback_data='2')],
            [InlineKeyboardButton("Избранное", callback_data='3')],
            [InlineKeyboardButton("Заказы", callback_data='4')],
            [InlineKeyboardButton("Добавить категорию", callback_data='5')],
            [InlineKeyboardButton("Добавить товар", callback_data='6')],
            [InlineKeyboardButton("Добавить админа", callback_data='7')],
            [InlineKeyboardButton("Удалить админа", callback_data='10')],
            [InlineKeyboardButton("Заказы, админ версия", callback_data='8')],
            [InlineKeyboardButton("Поиск по названию", callback_data='9')],
            [InlineKeyboardButton("Наши контакты", callback_data='11')]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=f'Рады вас приветствовать, {user.first_name}, расскажем немного о себе! '
                                             f'Уже 11 лет мы профессионально помогаем совершать покупки за рубежом🫶🏻 '
                                             f'Одеваться стильно и ни в чем себе не отказывать! У нас вы можете '
                                             f'встретить только 100% оригинальные брендовые вещи, все товары '
                                             f'заказываются из официальных интернет-магазинов брендов, а также на мировых '
                                             f'мультибрендовых сайтах. По запросу мы предоставим инвойс (чек о покупке). ',

                                  reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = update.effective_user
    await query.answer()
    if query.data == '1':
        keyboard = []
        cats = session.query(Categories).all()
        cats = session.query(Categories).filter(Categories.family == None)
        for cat in cats:
            keyboard.append([InlineKeyboardButton(f"{cat.name}", callback_data=f'cat_{cat.id}')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text='Выберете категорию: ', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Выберете категорию: ', reply_markup=reply_markup)

    if query.data == '11':
        if update.message is not None:
            await update.message.reply_text(text='☎️💖 Наш номер для связи по всем вопросам: whatsup +79181724444\nА так же наш'
                                                 ' канал: https://t.me/mashgamash \nВк: https://vk.com/mash.gamash \n'
                                                 '#отзывы о нас собраны в наших сообществах ВК '
                                                 'https://vk.com/album-32162783_285703116 и ИГ '
                                                 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ0Nzk3NTkyMDMzMzQ3?story_media_id=2901076547017246090&igshid=YmMyMTA2M2Y=')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='☎️💖 Наш номер для связи по всем вопросам: whatsup +79181724444\nА так же наш'
                                                 ' канал: https://t.me/mashgamash \nВк: https://vk.com/mash.gamash \n'
                                                 '#отзывы о нас собраны в наших сообществах ВК '
                                                 'https://vk.com/album-32162783_285703116 и ИГ '
                                                 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTQ0Nzk3NTkyMDMzMzQ3?story_media_id=2901076547017246090&igshid=YmMyMTA2M2Y=')

    elif query.data == '2':
        userr = update.effective_user
        user = session.query(User).filter(User.username == userr.username).first()
        if user:
            bask = session.query(Basket).filter(Basket.user_id == user.id)
            if bask:
                for b in bask:
                    good = session.query(Goods).filter(Goods.id == b.goods_id).first()
                    if good.sale < 1.0:
                        f_p = good.price - (good.sale * good.price)
                    else:
                        f_p = good.price
                    text = f'{good.name} \n'  \
                    f'{good.desc} \n' \
                    f'ЦЕНА: {f_p } + доставка из США ' \
                    f'(из расчета 230 р. за 100 гр.) \n'
                    if good.size:
                        text += f'Размер {good.size} \n'
                    if good.count:
                        text += f'Наличие {good.count} шт. \n'

                    keyboard = [[InlineKeyboardButton(f"Добавить этот товар еще",
                                                      callback_data=f'good_{good.id}_add_{user.id}')],
                                [InlineKeyboardButton(f"Удалить товар",
                                                      callback_data=f'good_{good.id}_del_{user.id}')],]

                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\mashgamash_shop_bot\\{good.pic}', "rb")),
                                                 caption=text, reply_markup=reply_markup,
                                                 chat_id=userr.id)

                keyboard = [[InlineKeyboardButton(f"Заказать",
                                                  callback_data=f'order_{user.id}')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if update.message is not None:
                    await update.message.reply_text(text='Заказать товары из корзины: ', reply_markup=reply_markup)
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(text='Заказать товары из корзины: ', reply_markup=reply_markup)
            else:
                if update.message is not None:
                    await update.message.reply_text(text='Ваша корзина пуста :(')
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(text='Ваша корзина пуста :(')

        else:
            if update.message is not None:
                await update.message.reply_text(text='Ваша корзина пуста :(')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(text='Ваша корзина пуста :(')

    elif query.data == '3':
        user = update.effective_user
        userr = session.query(User).filter(User.username == user.username).first()
        if userr:
            bask = session.query(Favorites).filter(Favorites.user_id == userr.id)
            if bask:
                for b in bask:
                    good = session.query(Goods).filter(Goods.id == b.goods_id).first()
                    if good.sale < 1.0:
                        f_p = good.price - (good.sale * good.price)
                    else:
                        f_p = good.price
                    text = f'{good.name} \n' \
                    f'{good.desc} \n' \
                    f'ЦЕНА: {f_p} + доставка из США ' \
                    f'(из расчета 230 р. за 100 гр.) \n'
                    if good.size:
                        text += f'Размер {good.size} \n'
                    if good.count:
                        text += f'Наличие {good.count} шт. \n'

                    keyboard = [[InlineKeyboardButton(f"Добавить этот товар в корзину",
                                                      callback_data=f'good_{good.id}_add_{userr.id}')],
                                [InlineKeyboardButton(f"Удалить товар",
                                                      callback_data=f'fav_{good.id}_del_{userr.id}')],]

                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\mashgamash_shop_bot\\{good.pic}', "rb")),
                                                 caption=text, reply_markup=reply_markup,
                                                 chat_id=user.id)

                keyboard = [[InlineKeyboardButton(f"Заказать",
                                                  callback_data=f'order_{userr.id}')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                # if update.message is not None:
                #     await update.message.reply_text(reply_markup=reply_markup)
                # elif update.callback_query is not None:
                #     await update.callback_query.message.reply_text(text='Заказать ', reply_markup=reply_markup)
            else:
                if update.message is not None:
                    await update.message.reply_text(text='У вас нет избранных товаров')
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(text='У вас нет избранных товаров')

        else:
            if update.message is not None:
                await update.message.reply_text(text='У вас нет избранных товаров')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(text='У вас нет избранных товаров')

    elif query.data == '4':
        userr = update.effective_user
        user = session.query(User).filter(User.username == userr.username).first()
        if user:
            ord = session.query(Orders).filter(Orders.username_customer == userr.username).all()
            keyboard = []
            if ord:
                for o in ord:
                    keyboard.append([InlineKeyboardButton(f"{o.id} заказ", callback_data=f'ord_{o.id}')])

                reply_markup = InlineKeyboardMarkup(keyboard)
                if update.message is not None:
                    await update.message.reply_text(reply_markup=reply_markup, text='Ваши заказы: ')
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(reply_markup=reply_markup, text='Ваши заказы: ')

            else:
                if update.message is not None:
                    await update.message.reply_text(text='У вас нет заказов')
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(text='У вас нет заказов')
        else:
            if update.message is not None:
                await update.message.reply_text(text='У вас нет заказов')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(text='У вас нет заказов')

    elif query.data.startswith('cat_'):
        id_cat = query.data.replace('cat_', '')
        cat = session.query(Categories).get(int(id_cat))
        sons = session.query(Categories).filter(Categories.family == int(cat.id)).all()
        keyboard = []
        user = update.effective_user
        result = await loop.run_in_executor(None, get_user, user)
        print(sons)
        if sons:
            for s in sons:
                keyboard.append([InlineKeyboardButton(f"{s.name}", callback_data=f'cat_{s.id}')])
            if result:
                keyboard.append([InlineKeyboardButton(f"Удалить категорию {cat.name}", callback_data=f'catdel_{cat.id}')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.message is not None:
                await update.message.reply_text(reply_markup=reply_markup, text=f'Категории {cat.name} ')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(reply_markup=reply_markup, text=f'Категории {cat.name} ')

        else:
            goods = session.query(Goods).filter(Goods.cat == cat.id)
            for good in goods:
                if good.sale < 1.0:
                    f_p = good.price - (good.sale * good.price)
                else:
                    f_p = good.price
                text = f'{good.name} \n' \
                f'{good.desc} \n' \
                f'ЦЕНА: {f_p } + доставка из США ' \
                f'(из расчета 230 р. за 100 гр.) \n'
                if good.size:
                    text += f'Размер {good.size} \n'
                if good.count:
                    text += f'Наличие {good.count} шт. \n'

                if get_user:
                    keyboard = [[InlineKeyboardButton(f"Добавить этот товар в корзину",
                                                      callback_data=f'good_{good.id}_add_{user.id}')],
                                [InlineKeyboardButton(f"Добавить в избранное",
                                                      callback_data=f'fav_{good.id}_add_{user.id}')],
                                [InlineKeyboardButton(f"Удалить товар",
                                                      callback_data=f'delprod_{good.id}')],
                                [InlineKeyboardButton(f"Изменить товар",
                                                      callback_data=f'updateprod_{good.id}')],
                                ]
                else:
                    keyboard = [[InlineKeyboardButton(f"Добавить этот товар в корзину",
                                                      callback_data=f'good_{good.id}_add_{user.id}')],
                                [InlineKeyboardButton(f"Добавить в избранное",
                                                      callback_data=f'fav_{good.id}_add_{user.id}')], ]

                reply_markup = InlineKeyboardMarkup(keyboard)
                if good.pic and not 'None' in good.pic and not 'null' in str(good.pic).lower():
                    await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\mashgamash_shop_bot\\{good.pic}', "rb")),
                                                 caption=text, reply_markup=reply_markup,
                                                 chat_id=user.id)
                else:
                    if update.message is not None:
                        await update.message.reply_text(
                            text=text, reply_markup=reply_markup)
                    elif update.callback_query is not None:
                        await update.callback_query.message.reply_text(text=text, reply_markup=reply_markup)

    elif query.data.startswith('delprod_'):
        good_id = int(query.data.replace('delprod_', ''))
        bas = session.query(Goods).filter(Goods.id == good_id).first()
        session.delete(bas)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text='Удалили товар!')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Удалили товар!')

    elif query.data.startswith('catdel_'):
        cat_id = int(query.data.replace('catdel_', ''))
        bas = session.query(Categories).filter(Categories.id == cat_id).first()
        session.delete(bas)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text='Удалили категорию, но товары не удалены с этой категорией :)')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Удалили категорию, но товары не удалены с этой категорией :)')

    elif query.data.startswith('updateprod_'):
        good_id = int(query.data.replace('updateprod_', ''))
        prod = session.query(Goods).filter(Goods.id == good_id).first()
        cat = session.query(Categories).filter(Categories.id == prod.cat).first()
        message = f'Используйте команду /upd_product для изменения товара, шаблон с данным товаром, измените то, что хотите изменить:\n' \
                  f'/upd_product id: {prod.id}; Название: {prod.name}; Описание: {prod.desc}; Цена: {prod.price}; Скидка: {prod.sale}; Размеры: {prod.size};' \
                  f'Наличие: {prod.count}; Категория: {cat};\n' \
                  f'Описание, скидку, размеры, кол-во и картинку можно не указывать. Если хотите добавить картинку, то ' \
                  f'этот шаблон видоизмененный надо отослать вместе с картинкой в одном сообщении. '
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)


    elif query.data.startswith('good_'):
        if 'add' in query.data:
            good_id = query.data.replace('good_', '')
            good_id = int(good_id[:good_id.find('_')])
            us = session.query(User.id).filter(User.username == user.username)
            bas = Basket(user_id=us, goods_id=good_id)
            session.add(bas)
            session.commit()
        elif 'del' in query.data:
            good_id = query.data.replace('good_', '')
            good_id = int(good_id[:good_id.find('_')])
            us = session.query(User.id).filter(User.username == user.username)
            bas = session.query(Basket).filter(Basket.user_id == us, Basket.goods_id == good_id).first()
            session.delete(bas)
            session.commit()

    elif query.data.startswith('fav_'):
        if 'del' in query.data:
            good_id = query.data.replace('fav_', '')
            good_id = int(good_id[:good_id.find('_')])
            us = session.query(User.id).filter(User.username == user.username)
            fav = session.query(Favorites).filter(Favorites.user_id == us, Favorites.goods_id == good_id).first()
            session.delete(fav)
            session.commit()
        elif 'add' in query.data:
            good_id = query.data.replace('fav_', '')
            good_id = int(good_id[:good_id.find('_')])
            us = session.query(User.id).filter(User.username == user.username)
            bas = Favorites(user_id=us, goods_id=good_id)
            session.add(bas)
            session.commit()

    elif query.data.startswith('order_'):
        us = session.query(User).filter(User.username == user.username).first()
        all_prods = session.query(Basket).filter(Basket.user_id == us.id).all()
        print(all_prods)
        text = []
        all_price = 0
        for prod in all_prods:
            good = session.query(Goods).filter(Goods.id == prod.goods_id).first()
            print(good)
            text.append(f'⭐️ {good.name} - цена: {good.price - (good.sale * good.price) }')
            all_price += good.price - (good.sale * good.price)
        message = '\n'.join(text)
        message += '\n \n \n' + f'Общая сумма: {float(all_price)}\nОформить заказ?'
        ord = Orders(user_id=user.id, username_customer=user.username, text_about=message, final_price=float(all_price))
        session.add(ord)
        session.commit()

        keyboard = [[InlineKeyboardButton(f"Оплатить", callback_data=f'pay_{ord.id}')],
                    [InlineKeyboardButton(f"Отменить", callback_data=f'delord_{ord.id}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(reply_markup=reply_markup, text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(reply_markup=reply_markup, text=message)

    elif query.data.startswith('delord_'):
        orde = query.data.replace('delord_', '')
        orde = int(orde)
        fav = session.query(Orders).filter(Orders.id == orde).first()
        session.delete(fav)
        session.commit()

    elif query.data.startswith('supp'):
        if update.message is not None:
            await update.message.reply_text(text='Напишите нам в поддержку по номеру whatsup: +79181724444 ⭐️🌛')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Напишите нам в поддержку по номеру whatsup: +79181724444 ⭐️🌛')

    elif query.data.startswith('pay_'):
        user = update.effective_user
        orde = query.data.replace('pay_', '')
        orde = int(orde)
        o = session.query(Orders).filter(Orders.id == orde).first()
        if update.message is not None:
            await update.message.reply_text(text=f'Для оплаты пройдитесь по пунктам:\n1) Пришлите ровно указанную сумму на эту карту: 5469400999485035, сохраните чек\n'
                                                 f'2) Напишите нашему менеджеру в whatsup +79181724444 с приложенным номером заказа {o.id} ⭐️🌛\n'
                                                 f'3) Далее ваш статус заказа измениться и с вами обсудят детали')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Для оплаты пройдитесь по пунктам:\n1) Пришлите ровно указанную сумму на эту карту: 5469400999485035, сохраните чек\n'
                                                 f'2) Напишите нашему менеджеру в whatsup с приложенным номером заказа {o.id} ⭐️🌛\n'
                                                 f'3) Далее ваш статус заказа измениться и с вами обсудят детали')

    elif query.data.startswith('ord_'):
        user = update.effective_user
        result = await loop.run_in_executor(None, get_user, user)
        orde = query.data.replace('ord_', '')
        orde = int(orde)
        o = session.query(Orders).filter(Orders.id == orde).first()
        message = f'Номер заказа: {o.id}\nПокупатель: @{o.username_customer}\nСтатус заказа: {o.paied}\n' \
                  f'Заказ: {o.text_about}'
        keyboard = [[InlineKeyboardButton(f"Написать в поддержку", callback_data=f'supp')]
                    ]
        if not o.paied and not result:
            keyboard.append([InlineKeyboardButton(f"Оплатить", callback_data=f'pay_{o.id}')])
        if result:
            keyboard.append([InlineKeyboardButton(f"Удалить заказ", callback_data=f'delord_{o.id}')])
            if not o.paied:
                keyboard.append([InlineKeyboardButton(f"Сменить статус на Оплаченый (будет True, а не False)", callback_data=f'chanord_{o.id}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text=message, reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message, reply_markup=reply_markup)

    elif query.data.startswith('chanord_'):
        orde = query.data.replace('chanord_', '')
        orde = int(orde)
        o = session.query(Orders).filter(Orders.id == orde).first()
        o.paied = True
        session.add(o)
        session.commit()

    elif query.data.startswith('pay_'):
        orde = query.data.replace('pay_', '')
        orde = int(orde)
        o = session.query(Orders).filter(Orders.id == orde).first()


    elif query.data == '5':
        message = 'Используйте команду /add_cat для создания новой категории, шаблон:\n' \
                  '/add_cat Название: Верхняя одежда; Родительская категория: одежда;\n' \
                  'Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == '6':
        message = 'Используйте команду /add_product для создания новой категории, шаблон:\n' \
                  '/add_product Название: Шляпка панамка; Описание: ааааааааа; Цена: 2000; Скидка: 0.2; Размеры: Xl, L, M;' \
                  'Наличие: 20; Категория: Головной убор;\n' \
                  'Описание, скидку, размеры, кол-во и картинку можно не указывать. Если хотите добавить картинку, то ' \
                  'этот шаблон видоизмененный надо отослать вместе с картинкой в одном сообщении. ' \
                  'Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == '7':
        message = 'Используйте команду /add_admin для добавления администратора, шаблон:\n' \
                  '/add_admin username;\n' \
                  'Пишите без @. Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == '8':
        keyboard = [[InlineKeyboardButton(f"Поиск по цене, юзеру, номеру заказа", callback_data=f'findord')],
                    [InlineKeyboardButton(f"Все заказы", callback_data=f'allord')]
                    ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text='Заказы', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Заказы', reply_markup=reply_markup)

    elif query.data == '9':
        message = 'Используйте команду /find_prod для поиска товара по названию, шаблон:\n' \
                  '/find_prod Adidas\n' \
                  'Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == '10':
        message = 'Используйте команду /deladm для удаления админа, шаблон:\n' \
                  '/deladm username\n' \
                  'Пишите ник без @. Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == 'findord':
        message = 'Используйте команду /findord для поиска по цене, юзеру, номеру заказа, шаблон:\n' \
                  '/findord 2000\n' \
                  '/findord username\n' \
                  'Советуем копировать шаблон :)'
        if update.message is not None:
            await update.message.reply_text(text=message)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=message)

    elif query.data == 'allord':
        ords = session.query(Orders).order_by(Orders.id.desc()).all()
        if ords:
            keyboard = []
            for s in ords:
                keyboard.append([InlineKeyboardButton(f"{s.id} заказ", callback_data=f'ord_{s.id}')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.message is not None:
                await update.message.reply_text(reply_markup=reply_markup, text=f'Заказы по вашему поиску')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(reply_markup=reply_markup,
                                                               text=f'Заказы по вашему поиску')
        else:
            if update.message is not None:
                await update.message.reply_text(text='Мы ничего не нашли :(')
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(text='Мы ничего не нашли :(')

async def add_cat(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)
    name = extract_value(mess, 'Название: ')
    family = extract_value(mess, 'Родительская категория: ')

    prod = Categories(name=name)
    if family:
        id_family = session.query(Categories).filter(Categories.name.ilike(f'%{family}%')).first()
        if id_family:
            prod.family = int(id_family.id)
    session.add(prod)
    session.commit()
    await update.message.reply_text('Теперь у вас новая категория :)')

async def add_product(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)
    name = extract_value(mess, 'Название: ')
    desc = extract_value(mess, 'Описание: ')
    price = extract_value(mess, 'Цена: ')
    sale = extract_value(mess, 'Скидка: ')
    sizes = extract_value(mess, 'Размеры: ')
    count = extract_value(mess, 'Наличие: ')
    cat = extract_value(mess, 'Категория: ')

    try:
        photo = update.message.photo[-1]
    except:
        photo = None
    file_path = None
    if photo:
        file_info = await context.bot.get_file(photo.file_id)
        id = file_info.file_id
        file_path = f"photos/{id}.jpg"  # Укажите путь и имя файла
        file_bytes = await file_info.download_as_bytearray()
        with open(file_path, "wb") as f:
            f.write(file_bytes)

    prod = Goods(name=name)
    if cat:
        id_family = session.query(Categories).filter(Categories.name.ilike(f'%{cat}%')).first()
        if id_family:
            prod.cat = int(id_family.id)
    if desc:
        prod.desc = desc
    if price:
        prod.price = float(int(price))
    if sale:
        prod.sale = float(sale)
    if sizes:
        prod.size = sizes
    if count:
        prod.count = int(count)
    if file_path:
        prod.pic = file_path
    session.add(prod)
    session.commit()
    await update.message.reply_text('Теперь у вас новый товар :)')

async def deladm(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)

    try:
        mess = mess.replace('/deladm', '')
    except:
        pass

    admin = session.query(Admins).filter(Admins.name == mess).first()
    session.delete(admin)
    session.commit()
    await update.message.reply_text('Админ удален')

async def upd_product(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)

    try:
        mess = mess.replace('/add_admin', '')
    except:
        pass

    id = extract_value(mess, 'id: ')
    name = extract_value(mess, 'Название: ')
    desc = extract_value(mess, 'Описание: ')
    price = extract_value(mess, 'Цена: ')
    sale = extract_value(mess, 'Скидка: ')
    sizes = extract_value(mess, 'Размеры: ')
    count = extract_value(mess, 'Наличие: ')
    cat = extract_value(mess, 'Категория: ')

    try:
        photo = update.message.photo[-1]
    except:
        photo = None
    file_path = None
    if photo:
        file_info = await context.bot.get_file(photo.file_id)
        id = file_info.file_id
        file_path = f"photos/{id}.jpg"  # Укажите путь и имя файла
        file_bytes = await file_info.download_as_bytearray()
        with open(file_path, "wb") as f:
            f.write(file_bytes)

    prod = session.query(Goods).filter(Goods.id == id).first()
    if cat and cat != prod.cat:
        id_family = session.query(Categories).filter(Categories.name.ilike(f'%{cat}%')).first()
        if id_family:
            prod.cat = int(id_family.id)
    if desc and desc != prod.desc:
        prod.desc = desc
    if name and name != prod.name:
        prod.name = name
    if price and price != prod.price:
        prod.price = float(price)
    if sale and sale!= prod.sale:
        prod.sale = float(sale)
    if sizes and sizes != prod.size:
        prod.size = sizes
    if count and count != prod.count:
        prod.count = int(count)
    if file_path and file_path != prod.pic:
        prod.pic = file_path
    session.add(prod)
    session.commit()
    await update.message.reply_text('Товар изменен :)')

async def add_admin(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)

    try:
        mess = mess.replace('/add_admin', '')
    except:
        pass

    adm = Admins(name=mess)
    session.add(adm)
    session.commit()
    await update.message.reply_text('Теперь у вас новый админ :)')

async def findord(update, context):
    text = update.message.caption
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)

    try:
        mess = mess.replace('/findord', '')
    except:
        pass

    try:
        mess = int(mess)
        ords = session.query(Orders).filter(Orders.id == mess).all()
    except:
        try:
            mess = float(mess)
            ords = session.query(Orders).filter(Orders.final_price == mess).all()
        except:
            ords = session.query(Orders).filter(or_(Orders.username_customer == mess, Orders.text_about.ilike(f'%{mess}%'))).all()
    if ords:
        keyboard = []
        for s in ords:
            keyboard.append([InlineKeyboardButton(f"{s.id} заказ", callback_data=f'ord_{s.id}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(reply_markup=reply_markup, text=f'Заказы по вашему поиску')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(reply_markup=reply_markup, text=f'Заказы по вашему поиску')
    else:
        await update.message.reply_text('Мы ничего не нашли :(')

async def find_prod(update, context):
    text = update.message.caption
    user = update.effective_user
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)

    try:
        mess = mess.replace('/find_prod', '')
    except:
        pass

    prods = session.query(Goods).filter(
        or_(Goods.name.ilike(f'%{mess}%'), Goods.desc.ilike(f'%{mess}%'))).all()
    if prods:
        for good in prods:
            if good.sale < 1.0:
                f_p = good.price - (good.sale * good.price)
            else:
                f_p = good.price
            text = f'{good.name} \n'
            f'{good.desc} \n'
            f'ЦЕНА: {f_p } + доставка из США '
            f'(из расчета 230 р. за 100 гр.) \n'
            if good.size:
                text += f'Размер {good.size} \n'
            if good.count:
                text += f'Наличие {good.count} шт. \n'

            keyboard = [[InlineKeyboardButton(f"Добавить этот товар в корзину",
                                              callback_data=f'good_{good.id}_add_{user.id}')],
                        [InlineKeyboardButton(f"Удалить товар",
                                              callback_data=f'good_{good.id}_del_{user.id}')], ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\mashgamash_shop_bot\\{good.pic}', "rb")),
                                         caption=text, reply_markup=reply_markup,
                                         chat_id=user.id)

    else:
        await update.message.reply_text('Мы ничего не нашли :(')

async def which_handler(update, context):
    text = update.message.caption
    if 'add_product' in text:
        await add_product(update, context)
    elif 'upd_product' in text:
        await upd_product(update, context)
def main() -> None:
    TOKEN = '6445135079:AAGAU_HhyXTMeCkbK2cNsRlIypr_o8Orjd0'
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    new_admin_handler = CommandHandler('add_cat', add_cat)
    application.add_handler(new_admin_handler)
    del_admin_handler = CommandHandler('add_product', add_product)
    application.add_handler(del_admin_handler)
    rule_handler = CommandHandler('deladm', deladm)
    application.add_handler(rule_handler)
    new_shop_handler = CommandHandler('upd_product', upd_product)
    application.add_handler(new_shop_handler)
    new_rullete_handler = CommandHandler('add_admin', add_admin)
    application.add_handler(new_rullete_handler)
    del_shop_handler = CommandHandler('findord', findord)
    application.add_handler(del_shop_handler)
    new_about_handler = CommandHandler('find_prod', find_prod)
    application.add_handler(new_about_handler)
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, which_handler))
    # запускаем приложение
    application.run_polling()


if __name__ == '__main__':
    main()