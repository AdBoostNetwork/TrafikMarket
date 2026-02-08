class Account():
    """аккаунт
    Хранится:
    1)id (tg id int)
    2)name (str max 50 smbols)
    3)tg_username (str max 50 smbols)
    4)avatar_filename (str max 50 smbols)
    5)current_balance (float)
    6)frozen_balance (float)
    7)ids_of_deals (list of ints)
    8)scs_count (int)
    9)id_of_trnactions (list of ints)
    10)id_of_announs (list of ints)
    11)ref_link (str max 50 smbols)
    12)ref_ids (list of ints)
    13)referi (int)
    14)is_banned (bool)


    Сoздается при нажатии /start в боте.
    """


class Trnaction():
    """
    1) trnaction_id (int)
    2) user_id (int)
    2) status (finished/in_progress/canceled)
    3) trnactn_time (datetime)
    4) summ (float)
    5) sys_msg (str) #для сохранения типа ошибки, чтобы админы могли помочь
    6) type (str) In/Out
    """



class Announ():
    """
    1) announ_id (int)
    2) announ_name (str)
    3) seller_id (int)
    4) price (float) (отображается до 2-3 знаков)
    5) topic (str)
    6) announ_imgs (list of str)
    7) status (in_moderating/moderated)
    """

class Channel(Announ):
    """
    channel_subject (str)
    subs_quant (int)
    requests_quant (int)
    chn_type (bool)
    chn_country (str)
    prafitabiltiy (int)
    entry_requests (bool)


    Фильтры каналов:

1. Тематика
Новости
Треш
Эро 18+
Криптовалюты
Букмекерство
Музыка
Юмор
Еда
Игры
Фильмы/Сериалы
Психология
Здоровье
Путешествия
Экономика

2. Подписчики/Охват -


3. Тип канала
Публичный
Приватный

4. Страна
Россия, Узбекистан, Беларусь, Казахстан

5. Цена
От - До

6. Доходность
От - До

Каналы с заявками на вступление ✅

[Сортировка будет работать по степеням важности

Цена > подписчики > охват > доходность]
    """

class Ad(Announ):
    """
    1)channel_subject (str)
    2)channel_country (str)
    3)audience_reach (int)
    4)cpm (int)
    5)er (int)


Фильтры рекламы:
1.Тематика
Новости
Треш
Эро 18+
Криптовалюты
Букмекерство
Музыка
Юмор
Еда
Игры
Фильмы/Сериалы
Психология
Здоровье
Путешествия
Экономика

2.страна
3.охват
4.цпм
5. ER
6.цена

[Сортировка будет работать по степеням важности
Цена > подписчики > охват > ER > cpm]
    """

class Traffik(Announ):
    """
    1)traff_subject(str)
    2)platform_from(str)
    3)traff_type(str)
    4)audience_type(str)
    5)audience_country(str)



    (Фильтры трафика:

1. Тематика
Новости/СМИ
Треш
Эро 18+
Букмекерство
Криптовалюты
Музыка
Игры
Видео и Фильмы
Психология
Еда и Кулинария
Здоровье и Фитнес
Экономика
Юмор и развлечения
Путешествия

2. Платформа
Telegram
TikTok
Instagram
VK
YouTube
Google
Facebook

3. Способ залива:
Поиск Telegram
Спам Telegram
Спам TikTok

4. Тип аудитории:
ЖЦА, М-ЦА

5. Страны: СНГ, Бурж

6. Цена
От - До)
    """

class Accs(Announ):
    """
    1)country (str)
    2)log_type (str)
    3)idle_time (str)
    4)acc_type (str)
    5)premium (str)
    6)quant_of_stars (str)
    7)gifts (bool)
    8)tg_lvl (int)

    (Фильтры для раздела аккаунтов

1. Страна (Добавь все страны из LolzTeam)

2. Тип входа:

По номеру
Tdata
Session+json

3. Отлега (день+/месяц+/год+/3года+/6 лет+)

4. Траст/новорег

5. Premium (нет/месяц/год/2 года)

6. Количество звезд

7. Наличие подарков (да/нет)

8 Уровень в Telegram)
    """


class Deal():
    """
    1) deal_id (int)
    2) seller_id (int)
    3) buyer_id (int)
    4) deal_name (str) (по типу "Продажа канала"/"Покупка аккаунта")
    5) cost (float)
    6) deal_info (str)
    6) type (str) (scs_completed/canceled/active/disputed/in_disput)
    7) chat (str)
    """

class Appeal_chat():
    """
    1) id (int)
    2) user_id (int)
    3) topic (dep/undep/announs/deals/acc/other)
    4) last_msg (str)
    5) last_msg_files (list[str]) список имен файлов, прикрепленный к ласт сообщению
    6) is_last_msg_from_user (bool)
    6) chat_filename (str) имя txt файла с чатом, лежащего на сервере
    7) files_folder_filename (str) имя папки в файлами к обращению
    8) status (open/closed)
    """


def acc_maker(user_id, ref_id):
    """
    Создает новый аккаунт
    Порядок действий:
    1) Создает ник
    2) Создает реф ссылку
    3) остальное заполняет нулями/пустыми списками
    4) Сохраняет акк в БД

    :param user_id:
    :param ref_id:
    :return: account
    """

def get_account_info(user_id, ref_id = None):
    """нкцию acc_maker
    Запускается при запуске бота. Если акка с таким id не существует, запускает фу

    :param user_id: tg_id (int)
    :param ref_id: refer_id (int)|None
    :return: account
    """


    "___________________________________"
    """Функционал бота для админов
    
/start-> приветствие с двумя кнопками
1) 'получить инфу об юзере'->запрашивает id/name юзера, если получает инт то это ади, если не инт, это юз.
после чего присылает сообщение с инфой об пользователе с двумя кнопками
1.1) 'Забанить/разбанить' -> меняет account.is_banned и обновляет инфу в сообщении 
1.2) 'Вернуться'-> возвращает к /start

2) Модерация объявлений: аналогично след пункту, но с объявлениями


3) 'Посмотреть открытые споры' -> выводит сообщение с 7 кнопками первые пять, это объекты deal.type==disputed, в сортировке deal.deal_id по возрастанию
3.1-2.5) 'спор по заказу 69'  -> меняет deal.type на in_disput (чтобы 2 админа не брали один спор) и выводит инфу по заказу и 2 кнопки:
3.1.1) 'Прав продавец' -> меняет deal.type на scs_completed, создает транзакции списывания денег у покупателя из account.frozen_balance
и пополнения у продавца в account.current_ballance. возвращает на 2.1
3.1.2) 'Прав покупатель' -> меняет deal.type на canceled, возвращает покупателю деньги из account.frozen_balance в account.current_ballance
3.6) 'Показать следующие 5 споров' -> показывает след 5 объявлений 
3.7) 'Вернуться' -> возвращает к /start

"""


    "___________________________________"
""" функционал для юзеров
/start-> приветствие семью кнопками по типу 

    открыть приложение
профиль     активные заказы
Пополнить     вывести
Зав. Заказы     поддержка

1)Тут без комментариев

2)'профиль' -> ник, балик, замороженный балик, процент успешных заказов

3)'мои сделки' -> выводит кнопками активные заказы (аналогично обращениям к админу)
3.1.1)'связаться с продавцом/покупателем' -> просит ввести сообщение
3.1.1.1) 'Отправить' ->   запрашивает текст сообщения и запускает sent_deal_msg
3.1.1.2) 'Отменить' -> возвращает к 3.1
3.1.2) подтвердить выполнение (только у покупателя)
3.1.3) Оспорить (у обеих сторон)
3.2) 'Вернуться' -> возвращает к /start

4)'Пополнить балланс' -> запрашивает сумму пополнения и запускает dep()

5)Вывести деньги 

6)зав заказы

7) 'Поддержка' - ссылка на бота с ТП
"""


"___________________________________"
"""Прочие функции бота:"""


def sent_deal_msg(user_to_id, text, deal_info):
    """
    Отправляет сообщение второму участнику сделки, сохраняет его в deal.chat
    :param user_to_id:
    :param text:
    :param deal_info:
    :return:
    """



def dep(summ):
    """
    Создает платеж и, после ответа от криптобота, создает объект типа trnaction, зачисляет деньги на балик и присылает уведомление в боте
    :param summ:(float) сумма депа
    :return:
    """

def undep(summ):
    """
    Списывает деньги со счета, создает объект типа trnaction и выводит деньги через платежку

    Возможно, надо будет в аргументы добавить адрес кошеля
    :param summ:
    :return:
    """
