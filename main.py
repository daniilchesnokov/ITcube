import sqlite3
from aiogram import Bot, types, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional
from datetime import date
from statistics import multimode
from random import randint
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
books = sqlite3.connect('books1.db')
sqlbooks = books.cursor()
def delt(el):
    el = str(el)
    el = el.replace('(', '')
    el = el.replace(')', '')
    el = el.replace(',', '')
    el = el.replace("'", '')
    return el
class UserState(StatesGroup):
    surname = State()
    name = State()
    clas = State()
    liter = State()
    password = State()
    no = State()
    sSurname = State()
    sTitle = State()
    stat = State()
    get = State()
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    people_id = message.chat.id
    books = sqlite3.connect('books1.db')
    sqlbooks = books.cursor()
    sql = "SELECT id FROM users WHERE id = ?"
    sqlbooks.execute(sql, (people_id,))
    data = sqlbooks.fetchone()
    if data is None:
        await message.answer('Я твой электронный помощник в библиотеке МАОУ СОШ №33')
        null = 'null'
        sqlbooks = books.cursor()
        sqlbooks.execute("SELECT a2 FROM secret WHERE a1 = 'count'")
        coun = sqlbooks.fetchone()
        coun = delt(coun)
        coun=int(coun)
        coun +=1
        sqlbooks.execute(f"UPDATE secret SET a2 = {coun} WHERE a1 = 'count' ")
        sqlbooks.execute(f"INSERT INTO users VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (coun, people_id, null, null, null, null, 'Ученик', 'На проверке', null, null, null, null))
        books.commit()
        await message.answer('Давай знакомиться! \nНапиши свою фамилию')
        await UserState.surname.set()
    else:
        await message.answer('Я твой электронный помощник в библиотеке МАОУ СОШ №33\nДоступные команды /info')
@dp.message_handler(state=UserState.surname)
async def surname(message: types.Message):
    surname = message.text
    people_id = message.chat.id
    sqlbooks = books.cursor()
    sql = "UPDATE users SET surname = ? WHERE id = ?"
    sqlbooks.execute(sql, (surname, people_id,))
    books.commit()
    await message.answer('Напиши своё имя')
    await UserState.name.set()
@dp.message_handler(state=UserState.name)
async def name(message: types.Message):
    name = message.text
    people_id = message.chat.id
    sqlbooks = books.cursor()
    sql = "UPDATE users SET name = ? WHERE id = ?"
    sqlbooks.execute(sql, (name, people_id,))
    books.commit()
    await message.answer('Напиши свой класс(без литера(без буквы))')
    await UserState.clas.set()
@dp.message_handler(state=UserState.clas)
async def clas(message: types.Message):
    clas = message.text
    people_id = message.chat.id
    sqlbooks = books.cursor()
    sql = "UPDATE users SET clas = ? WHERE id = ?"
    sqlbooks.execute(sql, (clas, people_id,))
    books.commit()
    await message.answer('Напиши свой литер(букву класса)')
    await UserState.liter.set()
@dp.message_handler(state=UserState.liter)
async def liter(message: types.Message):
    liter = message.text.lower()
    people_id = message.chat.id
    sqlbooks = books.cursor()
    sql = "UPDATE users SET liter = ? WHERE id = ?"
    sqlbooks.execute(sql, (liter, people_id,))
    books.commit()
    await message.answer('Ты зарегестрирован \nУчётная запись проходит проверку\nДоступные команды /info')
    sqlbooks = books.cursor()
    sql = "SELECT id FROM users WHERE role = ?"
    sqlbooks.execute(sql, ('Модератор',))
    id_moder = sqlbooks.fetchone()
    if id_moder is None:
        pass
    else:
        people_id = str(people_id)
        sqlbooks = books.cursor()
        sql = "SELECT surname FROM users WHERE id = ?"
        sqlbooks.execute(sql, (people_id,))
        surname = sqlbooks.fetchone()
        surname = delt(surname)
        sqlbooks = books.cursor()
        sql = "SELECT name FROM users WHERE id = ?"
        sqlbooks.execute(sql, (people_id,))
        name = sqlbooks.fetchone()
        name = delt(name)
        sqlbooks = books.cursor()
        sql = "SELECT clas FROM users WHERE id = ?"
        sqlbooks.execute(sql, (people_id,))
        clas = sqlbooks.fetchone()
        clas = delt(clas)
        sqlbooks = books.cursor()
        sql = "SELECT liter FROM users WHERE id = ?"
        sqlbooks.execute(sql, (people_id,))
        liter = sqlbooks.fetchone()
        liter = delt(liter)
        mess = 'Новая регистрация: \nID ' + people_id + '\n' + 'Фамилия ' + surname + '\n' + 'Имя ' + name + '\n' + 'Класс ' + clas + liter+'\n'+'Укажите статус аккаунта!'
        id_moder = delt(id_moder)
        moderk = InlineKeyboardMarkup(row_width=1)
        Button = InlineKeyboardButton(text='На проверке', callback_data='m/1/'+people_id)
        Button2 = InlineKeyboardButton(text='Активный', callback_data='m/2/'+people_id)
        Button3 = InlineKeyboardButton(text='Подозрительный', callback_data='m/3/'+people_id)
        moderk.add(Button, Button2, Button3)
        await bot.send_message(id_moder, mess, reply_markup=moderk)
        await UserState.no.set()
@dp.callback_query_handler(text_contains='m')
async def send_random_value(callback: types.CallbackQuery):
    a = callback.data.split('/')
    otvet = a[1]
    id_user = a[2]
    if otvet == '1':
        status = 'На проверке'
    if otvet == '2':
        status = 'Активный'
    if otvet == '3':
        status = 'Подозрительный'
    sqlbooks = books.cursor()
    sql = "UPDATE users SET status = ? WHERE id = ?"
    sqlbooks.execute(sql, (status, id_user,))
    books.commit()
    await bot.send_message(id_user, f'Проверка аккаунта пройдена \nТекущий статус аккаунта-{status}')
@dp.message_handler(commands=['role'], state='*')
async def start(message: types.Message):
    await message.answer('Введи пароль для изменения роли')
    await UserState.password.set()
@dp.message_handler(state=UserState.password)
async def clas(message: types.Message):
    password = message.text
    sqlbooks = books.cursor()
    sql = "SELECT a2 FROM secret WHERE a2 = ?"
    sqlbooks.execute(sql, (password,))
    a2 = sqlbooks.fetchone()
    if a2 is None:
        await message.answer('Введён неверный пароль')
    else:
        a2 = delt(a2)
        roles = ["Модератор", "Сотрудник", "Администратор", "Ученик", "сотрудник"]
        a = '0'
        for i in roles:
            if a2 == i:
                rol = i
                a = '1'
        if a =='0':
            await message.answer('Введён неверный пароль')
        else:
            sqlbooks = books.cursor()
            sql = "SELECT a1 FROM secret WHERE a2 = ?"
            sqlbooks.execute(sql, (password,))
            a1 = sqlbooks.fetchone()
            a1 = delt(a1)
            people_id = message.chat.id
            sql = "UPDATE users SET role = ? WHERE id = ?"
            sqlbooks.execute(sql, (a1, people_id,))
            books.commit()
            await message.answer(f'Ваша роль изменена\nТекущая роль- {rol}')
            sqlbooks = books.cursor()
            sql = "SELECT id FROM users WHERE role = ?"
            sqlbooks.execute(sql, ('Администратор',))
            id_admin = sqlbooks.fetchone()
            if id_admin is None:
                pass
            else:
                people_id = str(people_id)
                sqlbooks = books.cursor()
                sql = "SELECT surname FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                surname = sqlbooks.fetchone()
                surname = delt(surname)
                sqlbooks = books.cursor()
                sql = "SELECT name FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                name = sqlbooks.fetchone()
                name = delt(name)
                sqlbooks = books.cursor()
                sql = "SELECT clas FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                clas = sqlbooks.fetchone()
                clas = delt(clas)
                sqlbooks = books.cursor()
                sql = "SELECT liter FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                liter = sqlbooks.fetchone()
                liter = delt(liter)
                mess = 'ID '+people_id+'\n'+'Фамилия '+surname+'\n'+'Имя '+name+'\n'+'Класс '+clas+liter+'\n'+'Новая роль '+a1
                id_admin = delt(id_admin)
                await bot.send_message(id_admin, mess)
                await UserState.no.set()
@dp.message_handler(commands=['searchsurname'], state='*')
async def send_searchsurname(message: types.Message):
    await message.answer('Введи интересующую тебя фамилию автора')
    await UserState.sSurname.set()
@dp.message_handler(state=UserState.sSurname)
async def searchsurname(message: types.Message):
    sqlbooks = books.cursor()
    sql = "SELECT title FROM books WHERE surname = ?"
    sqlbooks.execute(sql, (message.text,))
    items = sqlbooks.fetchall()
    if items == []:
        await message.answer('Такого автора нет')
    else:
        mess = ''
        for el in items:
            el = delt(el)
            mess = mess+el+'\n'
        await message.answer(mess)
        await UserState.no.set()
@dp.message_handler(commands=['searchtitle'], state='*')
async def send_searchtitle(message: types.Message):
    await message.answer('Введи интересующую тебя книгу')
    await UserState.sTitle.set()
@dp.message_handler(state=UserState.sTitle)
async def searchsurname(message: types.Message):
    sqlbooks = books.cursor()
    sql = "SELECT surname FROM books WHERE title = ?"
    sqlbooks.execute(sql, (message.text,))
    items = sqlbooks.fetchone()
    if items == []:
        await message.answer('Такой книги нет')
    else:
        sql = "SELECT surname FROM books WHERE title = ?"
        sqlbooks.execute(sql, (message.text,))
        items = sqlbooks.fetchone()
        el = delt(items)
        v = 'Автор- ' +str(el)
        sql1 = "SELECT genre FROM books WHERE title = ?"
        sqlbooks.execute(sql1, (message.text,))
        items = sqlbooks.fetchone()
        el = delt(items)
        sql1 = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql1, (el,))
        items = sqlbooks.fetchone()
        el = delt(items)
        v1 = 'Жанр- ' +str(el)
        sql2 = "SELECT ywriting FROM books WHERE title = ?"
        sqlbooks.execute(sql2, (message.text,))
        items = sqlbooks.fetchone()
        el = delt(items)
        v2 = 'Год написания- ' +str(el)
        sql3 = "SELECT quantily FROM books WHERE title = ?"
        sqlbooks.execute(sql3, (message.text,))
        items = sqlbooks.fetchone()
        el = delt(items)
        v3 = 'Количество- ' +str(el)
        sql4 = "SELECT description FROM books WHERE title = ?"
        sqlbooks.execute(sql4, (message.text,))
        items = sqlbooks.fetchone()
        el = delt(items)
        v4 = 'Описание: ' +str(el)
        mess = v+'\n'+v1+'\n'+v2+'\n'+v3+'\n'+v4
        await message.answer(mess)
        await UserState.no.set()
@dp.message_handler(commands=['status'], state='*')
async def start(message: types.Message):
    await message.answer('Введи пароль для изменения статуса')
    await UserState.stat.set()
@dp.message_handler(state=UserState.stat)
async def clas(message: types.Message):
    password = message.text
    sqlbooks = books.cursor()
    sql = "SELECT a2 FROM secret WHERE a2 = ?"
    sqlbooks.execute(sql, (password,))
    a2 = sqlbooks.fetchone()
    if a2 is None:
        await message.answer('Введён неверный пароль')
    else:
        a2 = delt(a2)
        states = ["Активный", "На проверке", "Подозрительный"]
        a = '0'
        for i in states:
            if a2 == i:
                stat = i
                a = '1'
        if a =='0':
            await message.answer('Введён неверный пароль')
        else:
            people_id = message.chat.id
            sqlbooks = books.cursor()
            sql = "SELECT a1 FROM secret WHERE a2 = ?"
            sqlbooks.execute(sql, (password,))
            a1 = sqlbooks.fetchone()
            a1 = delt(a1)
            sql = "UPDATE users SET status = ? WHERE id = ?"
            sqlbooks.execute(sql, (a1, people_id,))
            books.commit()
            await message.answer('Статус аккаунта успешно изменён')
            sqlbooks = books.cursor()
            sql = "SELECT id FROM users WHERE role = ?"
            sqlbooks.execute(sql, ('Администратор',))
            id_admin = sqlbooks.fetchone()
            if id_admin is None:
                pass
            else:
                people_id = str(people_id)
                sqlbooks = books.cursor()
                sql = "SELECT surname FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                surname = sqlbooks.fetchone()
                surname = delt(surname)
                sqlbooks = books.cursor()
                sql = "SELECT name FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                name = sqlbooks.fetchone()
                name = delt(name)
                sqlbooks = books.cursor()
                sql = "SELECT clas FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                clas = sqlbooks.fetchone()
                clas = delt(clas)
                sqlbooks = books.cursor()
                sql = "SELECT liter FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                liter = sqlbooks.fetchone()
                liter = delt(liter)
                sqlbooks = books.cursor()
                sql = "SELECT role FROM users WHERE id = ?"
                sqlbooks.execute(sql, (people_id,))
                role = sqlbooks.fetchone()
                role = delt(role)
                mess = 'Изменение статуса аккаунта с помощью пароля\n'+'ID '+people_id+'\n'+'Фамилия '+surname+'\n'+'Имя '+name+'\n'+'Класс '+clas+liter+'\n'+'Роль '+role+'\nНовый статус- '+stat
                id_admin = delt(id_admin)
                await bot.send_message(id_admin, mess)
                await UserState.no.set()
@dp.message_handler(commands='get', state='*')
async def get1(message: types.Message):
    await message.answer('Введите название книги, которую вы хотите взять')
    await UserState.get.set()
@dp.message_handler(state=UserState.get)
async def get2(message: types.Message):
    title1 = message.text
    sqlbooks = books.cursor()
    sql = "SELECT title FROM books WHERE title = ?"
    sqlbooks.execute(sql, (title1,))
    title = sqlbooks.fetchone()
    if title is None:
        await message.answer('Данная книга отсутствует в нашей библиотеке')
    else:
        title = delt(title)
        sqlbooks = books.cursor()
        sql = "SELECT quantily FROM books WHERE title = ?"
        sqlbooks.execute(sql, (title,))
        quantily = sqlbooks.fetchone()
        quantily = delt(quantily)
        quantily = int(quantily)
        if quantily <1:
            await message.answer('Свободные экземпляры данной книги закончились')
        else:
            people_id = message.chat.id
            sqlbooks = books.cursor()
            sql = "SELECT status FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            status = sqlbooks.fetchone()
            status = delt(status)
            if status != 'Активный' or status == 'Подозрительный':
                await message.answer('Статус вашего аккаунта не позволяет получить книгу')
            else:
                sqlbooks = books.cursor()
                sql = "SELECT id FROM users WHERE role = ?"
                sqlbooks.execute(sql, ('Сотрудник',))
                id_worker = sqlbooks.fetchone()
                if id_worker is None:
                    await message.answer('В данный момент библиотека не работает')
                else:
                    sqlbooks = books.cursor()
                    sql = "SELECT surname FROM users WHERE id = ?"
                    sqlbooks.execute(sql, (people_id,))
                    surname = sqlbooks.fetchone()
                    surname = delt(surname)
                    sqlbooks = books.cursor()
                    sql = "SELECT name FROM users WHERE id = ?"
                    sqlbooks.execute(sql, (people_id,))
                    name = sqlbooks.fetchone()
                    name = delt(name)
                    sqlbooks = books.cursor()
                    sql = "SELECT clas FROM users WHERE id = ?"
                    sqlbooks.execute(sql, (people_id,))
                    clas = sqlbooks.fetchone()
                    clas = delt(clas)
                    sqlbooks = books.cursor()
                    sql = "SELECT liter FROM users WHERE id = ?"
                    sqlbooks.execute(sql, (people_id,))
                    liter = sqlbooks.fetchone()
                    liter = delt(liter)
                    sqlbooks = books.cursor()
                    sql = "SELECT liter FROM users WHERE id = ?"
                    sqlbooks.execute(sql, (people_id,))
                    liter = sqlbooks.fetchone()
                    liter = delt(liter)
                    sqlbooks = books.cursor()
                    sql = "SELECT id FROM books WHERE title = ?"
                    sqlbooks.execute(sql, (title,))
                    id_book = sqlbooks.fetchone()
                    id_book = delt(id_book)
                    people_id = str(people_id)
                    mess = 'ID ' + people_id + '\n' + 'Фамилия ' + surname + '\n' + 'Имя ' + name + '\n' + 'Класс ' + clas + liter+'\nВыдать книгу \n"'+title1+'"?'
                    id_worker = delt(id_worker)
                    workerk = InlineKeyboardMarkup(row_width=2)
                    Button = InlineKeyboardButton(text='ДА', callback_data='g/yes/'+people_id+'/'+id_book)
                    Button2 = InlineKeyboardButton(text='НЕТ', callback_data='g/no/'+people_id+'/'+id_book)
                    workerk.add(Button, Button2)
                    await bot.send_message(id_worker, mess, reply_markup=workerk)
                    await UserState.no.set()
@dp.callback_query_handler(text_contains='g')
async def send_random_value(callback: types.CallbackQuery):
    a = callback.data.split('/')
    otvet = a[1]
    id_user = a[2]
    id_book = a[3]
    if otvet == 'no':
        await bot.send_message(id_user, 'К сожалению вам отказано в получении книги')
    else:
        data = date.today()
        sql = "UPDATE users SET id_book = ? WHERE id = ?"
        sqlbooks = books.cursor()
        sqlbooks.execute(sql, (id_book, id_user,))
        books.commit()
        sql = "UPDATE users SET data_book = ? WHERE id = ?"
        sqlbooks = books.cursor()
        sqlbooks.execute(sql, (data, id_user,))
        books.commit()
        await bot.send_message(id_user, 'Поздравляю с получением книги')
        sqlbooks = books.cursor()
        sql = "SELECT history FROM users WHERE id = ?"
        sqlbooks.execute(sql, (id_user,))
        history1 = sqlbooks.fetchone()
        history1 = delt(history1)
        sqlbooks = books.cursor()
        sql = "SELECT quantily FROM books WHERE id = ?"
        sqlbooks.execute(sql, (id_book,))
        quantily = sqlbooks.fetchone()
        quantily = delt(quantily)
        quantily = int(quantily)
        quantily = quantily-1
        sqlbooks = books.cursor()
        sql = "UPDATE books SET quantily = ? WHERE id = ?"
        sqlbooks.execute(sql, (quantily, id_book,))
        books.commit()
        if history1 == 'null':
            history1 = ''
            history = history1+id_book+';'
            sql = "UPDATE users SET history = ? WHERE id = ?"
            sqlbooks = books.cursor()
            sqlbooks.execute(sql, (history, id_user,))
            books.commit()
        sqlbooks = books.cursor()
        sql = "SELECT history FROM users WHERE id = ?"
        sqlbooks.execute(sql, (id_user,))
        history = sqlbooks.fetchone()
        history = delt(history)
        history = history.split(sep=';')
        lst = []
        for i in history:
            sql = "SELECT genre FROM books WHERE id = ?"
            sqlbooks.execute(sql, (i,))
            genre = sqlbooks.fetchone()
            genre = delt(genre)
            lst.append(genre)
        bestGenre = multimode(lst)
@dp.message_handler(commands='return', state='*')
async def retur(message: types.Message):
    id_user = message.chat.id
    sqlbooks = books.cursor()
    sql = "SELECT id_book FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    id_book = sqlbooks.fetchone()
    id_book = delt(id_book)
    if id_book == 'null':
        await message.answer('У тебя отсутствует активная книга')
    else:
        sqlbooks = books.cursor()
        sql = "SELECT id FROM users WHERE role = ?"
        sqlbooks.execute(sql, ('Сотрудник',))
        id_worker = sqlbooks.fetchone()
        if id_worker is None:
            await message.answer('В данный момент библиотека не работает')
        else:
            people_id = id_user
            sqlbooks = books.cursor()
            sql = "SELECT title FROM books WHERE id = ?"
            sqlbooks.execute(sql, (id_book,))
            title_book = sqlbooks.fetchone()
            title_book = delt(title_book)
            sqlbooks = books.cursor()
            sql = "SELECT surname FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            surname = sqlbooks.fetchone()
            surname = delt(surname)
            sqlbooks = books.cursor()
            sql = "SELECT name FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            name = sqlbooks.fetchone()
            name = delt(name)
            sqlbooks = books.cursor()
            sql = "SELECT clas FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            clas = sqlbooks.fetchone()
            clas = delt(clas)
            sqlbooks = books.cursor()
            sql = "SELECT liter FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            liter = sqlbooks.fetchone()
            liter = delt(liter)
            sqlbooks = books.cursor()
            sql = "SELECT liter FROM users WHERE id = ?"
            sqlbooks.execute(sql, (people_id,))
            liter = sqlbooks.fetchone()
            liter = delt(liter)
            people_id= str(people_id)
            mess = 'ID ' + people_id + '\n' + 'Фамилия ' + surname + '\n' + 'Имя ' + name + '\n' + 'Класс ' + clas + liter + '\nВозвращает книгу \n"' + title_book
            id_worker = delt(id_worker)
            workerk = InlineKeyboardMarkup(row_width=2)
            Button = InlineKeyboardButton(text='ДА', callback_data='r/yes/' + people_id + '/' + id_book)
            Button2 = InlineKeyboardButton(text='НЕТ', callback_data='r/no/' + people_id + '/' + id_book)
            workerk.add(Button, Button2)
            await bot.send_message(id_worker, mess, reply_markup=workerk)
@dp.callback_query_handler(text_contains='r')
async def send_random_value(callback: types.CallbackQuery):
    a = callback.data.split('/')
    otvet = a[1]
    id_user = a[2]
    id_book = a[3]
    sqlbooks = books.cursor()
    sql = "SELECT id FROM users WHERE role = ?"
    sqlbooks.execute(sql, ('Сотрудник',))
    id_worker = sqlbooks.fetchone()
    if id_worker is None:
        await bot.send_message(id_user, 'В данный момент библиотека не работает')
    else:
        await bot.send_message(id_user, 'Ожидайте подтверждение сотрудника')
        if otvet == 'no':
            await bot.send_message(id_user, 'К сожалению сотрудник не подтвердил возрат книги')
        else:
            sqlbooks = books.cursor()
            sql = "SELECT quantily FROM books WHERE id = ?"
            sqlbooks.execute(sql, (id_book,))
            quantily = sqlbooks.fetchone()
            quantily = delt(quantily)
            quantily = int(quantily)
            quantily = quantily + 1
            sqlbooks = books.cursor()
            sql = "UPDATE books SET quantily = ? WHERE id = ?"
            sqlbooks = books.cursor()
            sqlbooks.execute(sql, (quantily, id_book,))
            books.commit()
            sqlbooks = books.cursor()
            sql = "UPDATE users SET id_book = ? WHERE id = ?"
            sqlbooks.execute(sql, ('null', id_user,))
            books.commit()
            sqlbooks = books.cursor()
            sql = "UPDATE users SET data_book = ? WHERE id = ?"
            sqlbooks.execute(sql, ('null', id_user,))
            books.commit()
            await bot.send_message(id_user, 'Вы вернули книгу')
@dp.message_handler(commands='recom', state='*')
async def retur(message: types.Message):
    id_user = message.chat.id
    sqlbooks = books.cursor()
    sql = "SELECT history FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    history = sqlbooks.fetchone()
    history = delt(history)
    if history == 'null':
        sqlbooks = books.cursor()
        sqlbooks.execute("SELECT genre_int FROM genre")
        ge = sqlbooks.fetchall()
        g = len(ge)
        title1 = randint(1, g)
        title2 = randint(1, g)
        while title2 == title1:
            title2 = randint(1, g)
        title3 = randint(1, g)
        while title3 == title1 or title3 == title2:
            title3 = randint(1, g)
        title4 = randint(1, g)
        while title4 == title1 or title4 == title2 or title4 == title3:
            title4 = randint(1, g)
        title5 = randint(1, g)
        while title5 == title1 or title5 == title2 or title5 == title3 or title5 == title4:
            title5 = randint(1, g)
        sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql, (title1,))
        genre1 = sqlbooks.fetchone()
        genre1 = delt(genre1)
        sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql, (title2,))
        genre2 = sqlbooks.fetchone()
        genre2 = delt(genre2)
        sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql, (title3,))
        genre3 = sqlbooks.fetchone()
        genre3 = delt(genre3)
        sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql, (title4,))
        genre4 = sqlbooks.fetchone()
        genre4 = delt(genre4)
        sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
        sqlbooks.execute(sql, (title5,))
        genre5 = sqlbooks.fetchone()
        genre5 = delt(genre5)
        sql = "SELECT title FROM books WHERE genre = ?"
        sqlbooks.execute(sql, (title1,))
        book1 = sqlbooks.fetchone()
        book1 = delt(book1)
        sql = "SELECT title FROM books WHERE genre = ?"
        sqlbooks.execute(sql, (title2,))
        book2 = sqlbooks.fetchone()
        book2 = delt(book2)
        sql = "SELECT title FROM books WHERE genre = ?"
        sqlbooks.execute(sql, (title3,))
        book3 = sqlbooks.fetchone()
        book3 = delt(book3)
        sql = "SELECT title FROM books WHERE genre = ?"
        sqlbooks.execute(sql, (title4,))
        book4 = sqlbooks.fetchone()
        book4 = delt(book4)
        sql = "SELECT title FROM books WHERE genre = ?"
        sqlbooks.execute(sql, (title5,))
        book5 = sqlbooks.fetchone()
        book5 = delt(book5)
        b1 = book1+ ' (' + genre1 + ')'
        b2 = book2 + ' (' + genre2 + ')'
        b3 = book3 + ' (' + genre3 + ')'
        b4 = book4 + ' (' + genre4 + ')'
        b5 = book5 + ' (' + genre5 + ')'
        mess = 'Рекомендуем к прочтению:'+'\n'+b1+'\n'+b2+'\n'+b3+'\n'+b4+'\n'+b5
        await message.answer(mess)
    else:
        history = history.split(sep=';')
        history.pop(-1)
        lst = []
        for i in history:
            sql = "SELECT genre FROM books WHERE id = ?"
            sqlbooks.execute(sql, (i,))
            genre = sqlbooks.fetchone()
            genre = delt(genre)
            lst.append(genre)
        bestGenre = multimode(lst)
        l = len(bestGenre)
        if l > 2:
            moda1 = bestGenre[-1]
            moda2 = bestGenre[-2]
            moda1 = str(moda1)
            moda2 = str(moda2)
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda1,))
            titleM1 = sqlbooks.fetchmany(size=2)
            book1 = titleM1[0]
            book1 = delt(book1)
            book2 = titleM1[1]
            book2 = delt(book2)
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda2,))
            titleM2 = sqlbooks.fetchmany(size=2)
            book3 = titleM2[0]
            book3 = delt(book3)
            book4 = titleM2[1]
            book4 = delt(book4)
            sql = "SELECT genre_int FROM genre"
            sqlbooks.execute(sql, )
            genre_int = sqlbooks.fetchall()
            for i in genre_int:
                i = delt(i)
                if i != moda1 and i != moda2:
                    moda3 = i
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda3,))
            book5 = sqlbooks.fetchone()
            book5 = delt(book5)
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda1,))
            genre1 = sqlbooks.fetchone()
            genre1 = delt(genre1)
            genre2 = genre1
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda2,))
            genre3 = sqlbooks.fetchone()
            genre3 = delt(genre3)
            genre4 = genre3
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda3,))
            genre5 = sqlbooks.fetchone()
            genre5 = delt(genre5)
            b1 = book1 + ' (' + genre1 + ')'
            b2 = book2 + ' (' + genre2 + ')'
            b3 = book3 + ' (' + genre3 + ')'
            b4 = book4 + ' (' + genre4 + ')'
            b5 = book5 + ' (' + genre5 + ')'
            mess = 'Рекомендуем к прочтению:' + '\n' + b1 + '\n' + b2 + '\n' + b3 + '\n' + b4 + '\n' + b5
            await message.answer(mess)
        elif l == 2:
            moda1 = bestGenre[0]
            moda2 = bestGenre[1]
            moda1 = str(moda1)
            moda2 = str(moda2)
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda1,))
            titleM1 = sqlbooks.fetchmany(size=2)
            book1 = titleM1[0]
            book1 = delt(book1)
            book2 = titleM1[1]
            book2 = delt(book2)
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda2,))
            titleM2 = sqlbooks.fetchmany(size=2)
            book3 = titleM2[0]
            book3 = delt(book3)
            book4 = titleM2[1]
            book4 = delt(book4)
            sql = "SELECT genre_int FROM genre"
            sqlbooks.execute(sql, )
            genre_int = sqlbooks.fetchall()
            for i in genre_int:
                i = delt(i)
                if i != moda1 and i != moda2:
                    moda3 = i
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda3,))
            book5 = sqlbooks.fetchone()
            book5 = delt(book5)
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda1,))
            genre1 = sqlbooks.fetchone()
            genre1 = delt(genre1)
            genre2 = genre1
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda2,))
            genre3 = sqlbooks.fetchone()
            genre3 = delt(genre3)
            genre4 = genre3
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda3,))
            genre5 = sqlbooks.fetchone()
            genre5 = delt(genre5)
            b1 = book1 + ' (' + genre1 + ')'
            b2 = book2 + ' (' + genre2 + ')'
            b3 = book3 + ' (' + genre3 + ')'
            b4 = book4 + ' (' + genre4 + ')'
            b5 = book5 + ' (' + genre5 + ')'
            mess = 'Рекомендуем к прочтению:' + '\n' + b1 + '\n' + b2 + '\n' + b3 + '\n' + b4 + '\n' + b5
            await message.answer(mess)
        else:
            moda1 = bestGenre[0]
            sql = "SELECT title FROM books WHERE genre = ?"
            sqlbooks.execute(sql, (moda1,))
            titleM1 = sqlbooks.fetchmany(size=5)
            book1 = titleM1[0]
            book1 = delt(book1)
            book2 = titleM1[1]
            book2 = delt(book2)
            book3 = titleM1[2]
            book3 = delt(book3)
            book4 = titleM1[3]
            book4 = delt(book4)
            book5 = titleM1[4]
            book5 = delt(book5)
            sql = "SELECT genre_text FROM genre WHERE genre_int = ?"
            sqlbooks.execute(sql, (moda1,))
            genre1 = sqlbooks.fetchone()
            genre1 = delt(genre1)
            genre2 = genre1
            genre3 = genre1
            genre4 = genre1
            genre5 = genre1
            b1 = book1 + ' (' + genre1 + ')'
            b2 = book2 + ' (' + genre2 + ')'
            b3 = book3 + ' (' + genre3 + ')'
            b4 = book4 + ' (' + genre4 + ')'
            b5 = book5 + ' (' + genre5 + ')'
            mess = 'Рекомендуем к прочтению:' + '\n' + b1 + '\n' + b2 + '\n' + b3 + '\n' + b4 + '\n' + b5
            await message.answer(mess)
@dp.message_handler(commands='genre', state='*')
async def genre(message: types.Message):
    sqlbooks = books.cursor()
    sql = "SELECT genre_text FROM genre"
    sqlbooks.execute(sql, )
    genre = sqlbooks.fetchall()
    mess = ''
    for i in genre:
        i = delt(i)
        mess = mess + '-'+i + '\n'
    mess = 'Доступные жанры:\n'+mess
    await message.answer(mess)
@dp.message_handler(commands='profile', state='*')
async def profile(message: types.Message):
    sqlbooks = books.cursor()
    id_user = message.chat.id
    sql = "SELECT surname FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    surname = delt(sqlbooks.fetchone())
    surname = 'Фамилия- ' + surname
    sql = "SELECT name FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    name = delt(sqlbooks.fetchone())
    name = "Имя- " + name
    sql = "SELECT clas FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    clas = delt(sqlbooks.fetchone())
    sql = "SELECT liter FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    liter = delt(sqlbooks.fetchone())
    clas = "Класс- " + clas + liter
    sql = "SELECT role FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    role = delt(sqlbooks.fetchone())
    role = "Роль- " + role
    sql = "SELECT status FROM users WHERE id = ?"
    sqlbooks.execute(sql, (id_user,))
    status = delt(sqlbooks.fetchone())
    status = "Статус аккаунта- " + status
    mess = 'Ваш профиль:\n' + surname + '\n' + name + '\n' + clas + '\n' + role + '\n' + status
    await message.answer(mess)
@dp.message_handler(commands='info', state='*')
async def profile(message: types.Message):
    mess = '/profile - Мой профиль\n/genre - Доступные жанры книг в библиотеке\n/searchsurname - Поиск произведений по фамилии автора\n/searchtitle - Поиск информации по названию произведения\n/recom - Рекомендованные книги к прочтению\n/get - Выбрать и получить книгу\n/return - Вернуть активную книгу\n/role - Изменение роли участника\n/status - Изменение статуса аккаунта'
    await message.answer(mess)
if __name__ == '__main__':
    executor.start_polling(dp)