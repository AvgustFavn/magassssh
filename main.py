import asyncio
import re
from random import randint

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
            [InlineKeyboardButton("Как заказать?", callback_data='1')],
             [InlineKeyboardButton("Мои заказы", callback_data='2')],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Как заказать?", callback_data='1')],
            [InlineKeyboardButton("Мои заказы", callback_data='2')],
            [InlineKeyboardButton("Посмотреть заказы", callback_data='4')],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=f'Рады вас приветствовать, {user.first_name}, здесь вы можете круглосуточно '
                                         f'иметь доступ к своим заказам и быстро заказать наши товары :)',

                                  reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = update.effective_user
    await query.answer()
    if query.data == '1':
        if update.message is not None:
            await update.message.reply_text(text='Как заказать?\n⭐️ Заскриньте товар, который вы хотите купить и '
                                                 'отправьте в бота, вместе с описанием цвета и размера этого товара '
                                                 '(если есть возможность выбрать).')

            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\1.jpg', "rb")), chat_id=user.id)
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\2.jpg', "rb")), chat_id=user.id)

            await update.message.reply_text(text='⚠️⛔️ВНИМАНИЕ: каждое сообщение - один '
                                                 'товар и одно фото, отправленные одним сообщением!⚠️⛔️')

            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\правильно.jpg', "rb")), chat_id=user.id, caption='Как правильно:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\неправильно.jpg', "rb")), chat_id=user.id,
                                         caption='Как НЕ правильно:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\заказы.jpg', "rb")), chat_id=user.id,
                                         caption='Так же вы можете посмотреть свои заказы:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\заказ.jpg', "rb")), chat_id=user.id,
                                         caption='Вверху номер вашего заказа\nСтатус заказа может быть "Создан" и '
                                                 '"Выкуплен". Создан - этап обговаривания о товаре с продавцом, до того '
                                                 'как продавец купит ваш заказ и отправит его. Выкуплен - значит '
                                                 'продавец уже купил его и скоро его вам его отправит')

            await update.message.reply_text(text='Для дополнительных вопросов свяжитесь с менеджером: Вотсап: +7 (918) '
                                                 '112-02-33 или продавцом: тг: @avelneda')


        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Так же вы можете посмотреть свои заказы:')

            await update.callback_query.message.reply_text(text='Как заказать?\n⭐️ Заскриньте товар, который вы хотите купить и '
                                                 'отправьте в бота, вместе с описанием цвета и размера этого товара '
                                                 '(если есть возможность выбрать).')

            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\1.jpg', "rb")), chat_id=user.id)
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\2.jpg', "rb")), chat_id=user.id)

            await update.callback_query.message.reply_text(text='⚠️⛔️ВНИМАНИЕ: каждое сообщение - один '
                                                 'товар и одно фото, отправленные одним сообщением!⚠️⛔️')

            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\правильно.jpg', "rb")), chat_id=user.id,
                                         caption='Как правильно:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\неправильно.jpg', "rb")), chat_id=user.id,
                                         caption='Как НЕ правильно:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\заказы.jpg', "rb")), chat_id=user.id,
                                         caption='Так же вы можете посмотреть свои заказы:')
            await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\заказ.jpg', "rb")), chat_id=user.id,
                                         caption='Вверху номер вашего заказа\nСтатус заказа может быть "Создан" и '
                                                 '"Выкуплен". Создан - этап обговаривания о товаре с продавцом, до того '
                                                 'как продавец купит ваш заказ и отправит его. Выкуплен - значит '
                                                 'продавец уже купил его и скоро его вам его отправит')

            await update.callback_query.message.reply_text(text='Для дополнительных вопросов свяжитесь с менеджером: Вотсап: +7 (918) '
                                                 '112-02-33 или продавцом: тг: @avelneda')

    if query.data == '2':
        ords = session.query(Orders).filter(Orders.username_customer == user.username).all()
        keyboard = []
        for o in ords:
            keyboard.append([InlineKeyboardButton(f"Заказ # {o.id}", callback_data=f'order_{o.id}')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text='Ваши заказы: ', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Ваши заказы: ', reply_markup=reply_markup)
    if query.data == '3':
        if update.message is not None:
            await update.message.reply_text(text='Напишите размер, цвет, если есть '
                                                 'возможность их выбрать, и только одно фото товара. Каждый товар нужно заказывать через бот отдельно.')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Напишите размер, цвет, если есть '
                                                 'возможность их выбрать, и только одно фото товара. Каждый товар нужно заказывать через бот отдельно.')

    if query.data == '4':
        ords = session.query(Orders).filter(Orders.status == 'Создан').all()
        keyboard = []
        for o in ords:
            keyboard.append([InlineKeyboardButton(f"Заказ # {o.id} НОВЫЙ!", callback_data=f'order_{o.id}')])
        ords = session.query(Orders).filter(Orders.status != 'Создан').all()
        for o in ords:
            keyboard.append([InlineKeyboardButton(f"Заказ # {o.id}", callback_data=f'order_{o.id}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text='Чтобы найти заказы от определенного покупателя, напишите его никнейм в бот, пример: @username', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Чтобы найти заказы от определенного покупателя, напишите его никнейм в бот, пример: @username', reply_markup=reply_markup)

    if 'order_' in query.data:
        id_order = int(query.data.replace('order_', ''))
        order = session.query(Orders).filter(Orders.id == id_order).first()
        keyboard = []
        text = f'Заказ # {order.id}\nСтатус: {order.status}\nСообщение от покупателя @{order.username_customer}: {order.text_about}'
        if get_user(user):
            if order.notes:
                text += f'\nВаша записка: {order.notes}'
            if order.status == 'Создан':
                keyboard.append([InlineKeyboardButton("Сменить статус заказа на 'Выкуплен'", callback_data=f'changestat_{order.id}')])
            keyboard.append([InlineKeyboardButton("Удалить заказ", callback_data=f'delord_{order.id}')])
            keyboard.append([InlineKeyboardButton("Сделать заметку для заказа", callback_data=f'donote_{order.id}')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            if order.check:
                await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\{order.check}', "rb")), caption=text,
                                         chat_id=user.id, reply_markup=reply_markup)
            else:
                if update.message is not None:
                    await update.message.reply_text(
                        text=text, reply_markup=reply_markup)
                elif update.callback_query is not None:
                    await update.callback_query.message.reply_text(
                        text=text, reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("Написать по-поводу заказа", callback_data=f'talkadmin')]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.message is not None:
                await update.message.reply_text(
                    text=text, reply_markup=reply_markup)
            elif update.callback_query is not None:
                await update.callback_query.message.reply_text(
                    text=text, reply_markup=reply_markup)
            # await context.bot.send_photo(photo=(open(f'{BASE_DIR}\\{order.check}', "rb")),
            #                              text=text,
            #                              chat_id=user.id, reply_markup=reply_markup)

    if 'donote_' in query.data:
        id_order = int(query.data.replace('donote_', ''))
        if update.message is not None:
            await update.message.reply_text(text=f'Напишите для добавления заметки "Заметка для заказа {id_order}:" и '
                                                 f'дальше текст заметки. Подойдет этот шаблон только для заказа под '
                                                 f'номером {id_order}')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Напишите для добавления заметки "Заметка для заказа {id_order}:" и '
                                                 f'дальше текст заметки. Подойдет этот шаблон только для заказа под '
                                                 f'номером {id_order}')

    if 'talkadmin' in query.data:
        if update.message is not None:
            await update.message.reply_text(text='Напишите по этому контакту +7 (918) 112-02-33 ')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Напишите по этому контакту +7 (918) 112-02-33 ')

    if 'changestat_' in query.data:
        id_order = int(query.data.replace('changestat_', ''))
        order = session.query(Orders).filter(Orders.id == id_order).first()
        order.status = 'Выкуплен'
        session.add(order)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text=f'Заказ # {id_order} считается выкупленым')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Заказ # {id_order} считается выкупленым')

    if 'delord_' in query.data:
        id_order = int(query.data.replace('delord_', ''))
        order = session.query(Orders).filter(Orders.id == id_order).first()
        session.delete(order)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text=f'Заказ # {id_order} удален')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Заказ # {id_order} удален')

async def new_order(update: Update, context: CallbackContext):
    text = update.message.caption or update.message.text
    try:
        mess = '' + text
    except:
        mess = ' '.join(context.args)
    user = update.effective_user
    if "Заметка для заказа" in mess:
        id_ord = mess[:mess.find(':')+1]
        id_ord = int(re.sub(r'\D', '', id_ord))
        order = session.query(Orders).filter(Orders.id == id_ord).first()
        note = mess[mess.find(':')+1:]
        print(note)
        order.notes = note
        session.add(order)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text=f'Вы добавили заметку в заказ')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Вы добавили заметку в заказ')

    elif '@' in mess:
        user = mess.replace('@', '')
        ords = session.query(Orders).filter(Orders.status == 'Создан', Orders.username_customer == user).all()
        keyboard = []
        for o in ords:
            keyboard.append([InlineKeyboardButton(f"Заказ # {o.id} НОВЫЙ!", callback_data=f'order_{o.id}')])
        ords = session.query(Orders).filter(Orders.status != 'Создан', Orders.username_customer == user).all()
        for o in ords:
            keyboard.append([InlineKeyboardButton(f"Заказ # {o.id}", callback_data=f'order_{o.id}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message is not None:
            await update.message.reply_text(text=f'Заказы от {user}', reply_markup=reply_markup)
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text=f'Заказы от {user}', reply_markup=reply_markup)

    else:

        order = Orders(user_id=user.id, username_customer=user.username, text_about=mess)
        # Проверяем, есть ли в сообщении медиа-файл
        if update.message.photo:
            photo = update.message.photo[-1]
            if photo:
                file_info = await context.bot.get_file(photo.file_id)
                id = file_info.file_id
                file_path = f"photos/{str(randint(1, 10000))}.jpg"  # Укажите путь и имя файла
                file_bytes = await file_info.download_as_bytearray()
                with open(file_path, "wb") as f:
                    f.write(file_bytes)
                order.check = file_path

        session.add(order)
        session.commit()
        if update.message is not None:
            await update.message.reply_text(text='Ваш заказ зарегистрирован, скоро с вами свяжутся!')
        elif update.callback_query is not None:
            await update.callback_query.message.reply_text(text='Ваш заказ зарегистрирован, скоро с вами свяжутся!')


def main() -> None:
    TOKEN = '6966685315:AAG-uapgLjkduWe4UQILbF2-qqAIwrLSfBM'
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, new_order))
    application.add_handler(button_handler)
    application.run_polling()


if __name__ == '__main__':
    main()