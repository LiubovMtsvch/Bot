from bs4 import BeautifulSoup as b
import telebot
import random
import requests
from telebot import types
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()
import wikipedia


bot = telebot.TeleBot('6972523221:AAHyluRSzg1bffTC9ExL6-1wYcjtEc1R3PE')


"MERCEDES POWER+"
response = requests.get(url="https://en.wikipedia.org/wiki/Mercedes_AMG_F1_W10_EQ_Power%2B",)
soup = BeautifulSoup(response.content, 'html.parser')
result = wikipedia.search("Mercedes F1 W10 EQ Power+ (2019)")
print(result[0])
first_p_tag = soup.find('p')

# Выводим текст первого тега <p>
print(first_p_tag.get_text())





news_history = []
def get_motorsport_news_titles():
    url = 'https://www.motorsport.com/f1/news/'

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_data = []

        seen_titles = set()  # Множество для хранения уникальных заголовков
        for news in soup.find_all(class_='ms-item__title-short'):
            title = news.text.strip()
            if title not in seen_titles:
                image_url = news.find_previous(class_='ms-item__picture').find('img')['src']
                full_news_url = news.find_parent('a')['href']
                news_data.append((title, image_url, full_news_url))
                seen_titles.add(title)


        for news in news_data:
            yield news
            news_history.append(news)

news_generator = get_motorsport_news_titles()

# Выводим одну новость при каждом запуске
next_news = next(news_generator, None)
if next_news:
    title, image_url, full_news_url = next_news
    print(title)
    print(image_url)
    print(full_news_url)

else:
    print("Новостей больше нет")



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)




    kb = types.InlineKeyboardMarkup(row_width=1)


    kb_news = types.InlineKeyboardButton(text='Новости F1', callback_data='news_f1')
    kb_cars = types.InlineKeyboardButton(text='Автомобили F1', callback_data='cars_f1')
    kb_biographies = types.InlineKeyboardButton(text='Биографии гонщиков',  callback_data='biography')
    kb.add(kb_cars, kb_biographies, kb_news)

    bot.send_message(message.chat.id, 'Здравствуйте, здесь будут публиковаться новости F-1. Выбирайте, что вас интересует:', reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):


# N   E   W    S
    if call.data == 'news_f1':

        next_news = next(news_generator, None)
        if next_news:
            title, image_url, full_news_url = next_news
            caption = f"{title}\n\n" f'Читать полностью: motorsport.com/{full_news_url}'
            kb_podr_full = types.InlineKeyboardMarkup()
            kb_skip = types.InlineKeyboardButton(text='Другая новость', callback_data='new_news')
            kb_previous = types.InlineKeyboardButton(text='Предыдущая новость', callback_data='previous_new')

            kb_podr_full.add(kb_previous, kb_skip)
            bot.send_photo(call.message.chat.id, image_url, caption=caption, reply_markup=kb_podr_full,
                           parse_mode='Markdown')

    if call.data == 'previous_new':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if news_history:
            # Получите предыдущую новость из истории
            previous_news = news_history.pop()
            title, image_url, full_news_url = previous_news
            caption = f"{title}\n\n" f'Читать полностью: motorsport.com/{full_news_url}'
            kb_podr_full = types.InlineKeyboardMarkup()
            kb_skip = types.InlineKeyboardButton(text='Другая новость', callback_data='new_news')
            kb_previous = types.InlineKeyboardButton(text='Предыдущая новость', callback_data='previous_new')
            kb_podr_full.add(kb_previous, kb_skip)
            bot.send_photo(call.message.chat.id, image_url, caption=caption, reply_markup=kb_podr_full,
                           parse_mode='Markdown')


    if call.data == 'new_news':
        next_news = next(news_generator, None)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if news_history:
            # Выводим предыдущую новость из истории
            previous_news = news_history[-1]  #?????????????????????????
            if next_news:
                title, image_url, full_news_url = next_news
                caption = f"{title}\n\n" f'Читать полностью: motorsport.com/{full_news_url}'
                kb_podr_full = types.InlineKeyboardMarkup()
                kb_skip = types.InlineKeyboardButton(text='Другая новость', callback_data='new_news')
                kb_previous = types.InlineKeyboardButton(text='Предыдущая новость', callback_data='previous_new')

                kb_podr_full.add(kb_previous, kb_skip)
                bot.send_photo(call.message.chat.id, image_url, caption=caption, reply_markup=kb_podr_full,
                               parse_mode='Markdown')


# B I O G R A P H Y


    if call.data =='biography':

        kb_bio = types.InlineKeyboardMarkup(row_width=1)
        kb_ayrton_senna = types.InlineKeyboardButton(text='Айртон Сенна', callback_data='a_senna')
        kb_niki_lauda = types.InlineKeyboardButton(text='Ники Лауда', callback_data='n_lauda')
        kb_alain_prost = types.InlineKeyboardButton(text='Ален Прост', callback_data='alain_prost')
        kb_michael_shumaher = types.InlineKeyboardButton(text='Михаэль Шумахер', callback_data='m_shumaher')
        kb_oscar_piastri = types.InlineKeyboardButton(text='Оскар Пиастри', callback_data='oscar_p')
        kb_bio.add(kb_michael_shumaher,kb_ayrton_senna, kb_alain_prost, kb_niki_lauda, kb_oscar_piastri)
        bot.send_message(call.message.chat.id, text='Выберите интересующего вас автогонщика:', reply_markup=kb_bio)


    if call.data == 'a_senna':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Сенна родился в Бразилии в 1960 году в богатой семье и начал гонять на картинге в возрасте 13 лет.'
                   'Он был трехкратным чемпионом Формулы-1 (1988, 1990 и 1991 годов).'
                   'Айртон выиграл Гран-при Бразилии в 1991 и 1993 годах. '
                   'В 1982 году Aйртон выиграл гонку в Формуле Форд, несмотря на то, что у него почти не было тормозов.'
                   'Сенна ставил автоспорт выше личной жизни. Женщин в жизни Сенны на самом деле было много – Пике совершенно зря беспокоился. '
                   'Однако семейного счастья бразилец так толком и не познал, и виной тому то, '
                   'что Айртон всегда предпочитал гонки девушкам.')
        back_button_2 = types.InlineKeyboardButton('Выбрать другого автогонщика', callback_data='back_2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button_2)
        with open('img/1_ayrton-senna.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

    if call.data == 'n_lauda':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Ники Лауда, австрийский автогонщик, был трехкратным чемпионом Формулы-1 (1975, 1977 и 1984 годов).'
                   'Он является единственным гонщиком в истории Формулы-1, который становился чемпионом за команды Ferrari и McLaren.'
                   'Ники также был успешным предпринимателем в авиации и основал авиакомпании Lauda Air, Niki и Lauda.'
                   'В 1976 году Лауда попал в аварию на Гран-при Германии, которая почти стоила ему жизни. Он вернулся на трассу всего через шесть недель после аварии и продолжил гонять.'
                   'Ники попал в серьезную аварию, из-за которой он получил множественные ожоги.Пройдет всего лишь полтора месяца, и '
                   'отважный гонщик с окровавленной повязкой на голове вновь ринется в бой, финишируя четвертым. Следующей победой '
                   'становится место на подиуме в США. ')
        back_button_2 = types.InlineKeyboardButton('Выбрать другого автогонщика', callback_data='back_2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button_2)
        with open('img/niki_lauda.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

    if call.data == 'alain_prost':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Ален Прост был французским гонщиком Формулы-1 и четырежды становился чемпионом мира.'
                   'Он выиграл Гран-при Франции в 1981, 1982, 1988 и 1993 годах.'
                   'Ален был известен своей точностью и умением экономить топливо на трассе .'
                   'В 1983 г. француз стал чуть ли не главным претендентом на чемпионство в "Формуле-1".'
                   ' Он лидировал весь сезон, однако его снова подвела машина. Это обстоятельство очень расстроило руководство «Рено»,'
                   ' которое расторгло контракт с Аленом. Любители гонок тоже перестали симпатизировать герою этой статьи. '
                   'В связи с этими событиями молодой человек просто был вынужден переехать из Франции в Швейцарию.'
                   'В 1997 году Ален снова вернулся в "Формулу-1", но уже не в качестве гонщика, а как глава команды «Прост Гран-при».')
        back_button_2 = types.InlineKeyboardButton('Выбрать другого автогонщика', callback_data='back_2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button_2)
        with open('img/alen_prost.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'm_shumaher':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Михаэль Шумахер - легенда автоспорта, семикратный чемпион мира в гонках “Формулы-1”.'
                   'Немецкий начал свою карьеру в автоспорте на педальном картинге в возрасте 4 лет. В 6 лет он '
                   'уже одержал свою первую победу в гонках.'
                   'В конце декабря 2013 года, катаясь на горных лыжах во французских Альпах, Шумахер получил серьезную травму головы, пробыв после этого несколько месяцев в коме. В апреле 2014 года стало известно, что ему стало лучше, его перевезли из больницы домой, однако по'
                   ' желанию семьи о состоянии его здоровья с тех пор нет практически никаких сообщений.'
                   'Шумахер был назван “Спортсменом года” в Германии 4 раза (1995, 2000, 2001, 2004) и “Спортсменом десятилетия” в 2000 году.'
                   'Михаэль Шумахер любит футбол и раньше регулярно участвовал в организации различных благотворительных матчей, в том числе с участием гонщиков, блистая в этих играх на поле.')
        back_button_2 = types.InlineKeyboardButton('Выбрать другого автогонщика', callback_data='back_2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button_2)
        with open('img/shumaher.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'oscar_p':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Оскар Пиастри - австралийский гонщик, который сейчас выступает в Формуле 1 за команду McLaren.'
                   'Он родился 6 апреля 2001 года и является первым гонщиком Формулы 1, родившимся в 21 веке.'
                   'В 2022 году он был признан лучшим гонщиком серии FIA Formula 2.'
                   'Первое знакомство Оскара с автомобилями началось в молодом возрасте, когда он участвовал в гонках на автомобилях с дистанционным управлением на соревнованиях национального уровня. В 2011 году он вошел в мир картинга,'
                   ' и подросток продолжил участвовать в различных соревнованиях по всей Австралии. ')
        back_button_2 = types.InlineKeyboardButton('Выбрать другого автогонщика', callback_data='back_2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button_2)
        with open('img/piastri.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

#  C A R S


    if call.data =='cars_f1':

        kb_cars = types.InlineKeyboardMarkup()
        kb_ferrari = types.InlineKeyboardButton(text='Ferrari', callback_data='ferrari')
        kb_mclaren = types.InlineKeyboardButton(text='McLaren', callback_data='mcLaren')
        kb_aston = types.InlineKeyboardButton(text='Aston Martin', callback_data='aston_martin')
        kb_red_bull = types.InlineKeyboardButton(text='Red bull', callback_data='red_bull')
        kb_mercedes = types.InlineKeyboardButton(text='Mercedes', callback_data='mercedes')


        kb_cars.add(kb_mercedes, kb_ferrari, kb_mclaren, kb_aston,kb_red_bull)
        bot.send_message(call.message.chat.id, text='Выберите интересующий вас автомобиль:', reply_markup=kb_cars)

    if call.data == 'mercedes':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_mercedess = types.InlineKeyboardMarkup(row_width=1)
        kb_mersf1_power = types.InlineKeyboardButton(text='Mercedes F1 W10 EQ Power+ (2019)', callback_data='mersf1_power')
        kb_mersf1_w11 = types.InlineKeyboardButton(text='Mercedes-AMG F1 W11 EQ Performance (2020)', callback_data='mersf1_w11')
        kb_mersf1_w12 = types.InlineKeyboardButton(text='Mercedes-AMG F1 W12 E Performance (2021)', callback_data='mersf1_w12')
        kb_mercedess.add(kb_mersf1_power, kb_mersf1_w11, kb_mersf1_w12)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль Мерседес F1', reply_markup=kb_mercedess)


    if call.data == 'mersf1_power':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Mercedes AMG F1 W10 EQ Power+ — гоночный автомобиль с открытыми колёсами в '
                   'Формуле-1, был разработан и построен командой конструктором Mercedes AMG Petronas'
                   ' Motorsport для участия в чемпионате мира Формулы-1 сезона 2019 года. Болид был'
                   ' оснащен двигателем Mercedes 2019 года спецификации, M10 EQ Power+. Пилотировали '
                   'в 2019 году болид британский пилот Льюис Хэмилтон, выступавший в команде седьмой год, '
                   'и финский Валттери Боттас, выступавший за команду третий год.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/power.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'mersf1_w11':
        bot.delete_message(call.message.chat.id, call.message.message_id)

        caption = ('Mercedes-AMG F1 W11 EQ Performance — гоночный автомобиль Формулы-1, спроектированный и построенный командой Mercedes-AMG Petronas F1 под руководством Джеймса Эллисона, Джона Оуэна, Майка Эллиотта, Лоика Серры, Эшли Уэй'
                   ' Эмилиано Джанджулио, Джаррода Мерфи и Эрик Бландин примет'
                   ' участие в чемпионате мира Формулы-1 2020 года. Машиной управляли Льюис Хэмилтон и'
                   ' Валттери Боттас, которые оставались в команде восьмой и четвертый '
                   'сезоны соответственно.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/amg-eq-perfomance.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)



    if call.data == 'mersf1_w12':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Mercedes-AMG F1 W12 E Performance, обычно сокращенно Mercedes W12, — гоночный '
                   'автомобиль Формулы-1, разработанный и построенный командой Mercedes-AMG Petronas '
                   'Formula One под руководством Джеймса Эллисона для участия в чемпионате мира Формулы-1'
                   ' 2021 года. Машиной управляли Льюис Хэмилтон и Валттери Боттас.[2] Автомобиль основан на Mercedes-AMG F1'
                   ' W11 EQ Performance, который выиграл чемпионат пилотов и конструкторов в предыдущем сезоне.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/mers-w12-perfomance.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


#  B A C K   B U T T O N  1

    if call.data == 'back':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_cars = types.InlineKeyboardMarkup()
        kb_ferrari = types.InlineKeyboardButton(text='Ferrari', callback_data='ferrari')
        kb_mclaren = types.InlineKeyboardButton(text='McLaren', callback_data='mcLaren')
        kb_aston = types.InlineKeyboardButton(text='Aston Martin', callback_data='aston_martin')
        kb_red_bull = types.InlineKeyboardButton(text='Red bull', callback_data='red_bull')
        kb_mercedes = types.InlineKeyboardButton(text='Mercedes', callback_data='mercedes')
        kb_bmw = types.InlineKeyboardButton(text='BMW', callback_data='bmw')

        kb_cars.add(kb_mercedes, kb_ferrari, kb_mclaren, kb_aston, kb_red_bull)
        bot.send_message(call.message.chat.id, text='Выберите интересующий вас автомобиль:', reply_markup=kb_cars)


#  B A C K   B U T T O N 2


    if call.data == 'back_2':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_bio = types.InlineKeyboardMarkup(row_width=1)
        kb_ayrton_senna = types.InlineKeyboardButton(text='Айртон Сенна', callback_data='a_senna')
        kb_niki_lauda = types.InlineKeyboardButton(text='Ники Лауда', callback_data='n_lauda')
        kb_alain_prost = types.InlineKeyboardButton(text='Ален Прост', callback_data='alain_prost')
        kb_michael_shumaher = types.InlineKeyboardButton(text='Михаэль Шумахер', callback_data='m_shumaher')
        kb_oscar_piastri = types.InlineKeyboardButton(text='Оскар Пиастри', callback_data='oscar_p')
        kb_bio.add(kb_ayrton_senna, kb_alain_prost, kb_niki_lauda, kb_oscar_piastri, kb_michael_shumaher)
        bot.send_message(call.message.chat.id, text='Выберите интересующего вас автогонщика:', reply_markup=kb_bio)





#  M    C     L     A   R     E   N
    if call.data == 'mcLaren':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_mclaren = types.InlineKeyboardMarkup(row_width=1)
        kb_m2b = types.InlineKeyboardButton(text='McLaren M2B', callback_data='kb_m2b')
        kb_m23 = types.InlineKeyboardButton(text='McLaren M23 ',
                                                   callback_data='kb_m23')
        kb_mp413 = types.InlineKeyboardButton(text='McLaren MP4/13',
                                                   callback_data='kb_mp4')
        kb_mclaren.add(kb_m2b,  kb_m23, kb_mp413)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль McLaren F1', reply_markup=kb_mclaren)


    if call.data == 'kb_m2b':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Команда McLaren представила свой первый гоночный автомобиль'
                   ' Формулы-1, McLaren M2B, в 1966 году1. Это был первый автомобиль Формулы-1 команды'
                   ' McLaren, основанной гонщиком Брюсом Маклареном. Шасси было сконструировано под руководством '
                   'Робина Херда на основе прототипа M2A. Однако, самым интересным фактом об этом автомобиле '
                   'является то, что он был построен на основе монокока из “малит”-алюминия, который был использован в авиации.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/mclaren_m2b.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

    if call.data == 'kb_m23':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('McLaren M23 - это гоночный автомобиль, разработанный Гордоном Коппаком с участием Джона Барнарда.'
                   ' Он был представлен в 1973 году и участвовал в чемпионатах мира Формулы-1 с 1973 по 1978 годы. '
                   'Автомобиль имел очень аэродинамически эффективные формы кузова, которые были вдохновлены моделью Lotus 72. ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/mclaren_23.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'kb_mp4':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('McLaren MP4/13 - это гоночный автомобиль, разработанный конструкторами Эдрианом Ньюи, '
                   'Стивом Николсом, Нилом Оутли и Анри Дюраном с участием Марио Иллиена. '
                   'Он был представлен в 1998 году и участвовал в чемпионатах мира Формулы-1 в том же году. '
                   'Автомобиль был оснащен двигателем Mercedes-Benz FO110G (72°), атмосферный, 3,0 л, V10, '
                   'мощностью 780-800 л.с. '
                   'Всего McLaren MP4/13 выиграл 9 гонок и одержал 12 поул-позиций.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/MP413.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

# M E R C E D E S



    if call.data == 'mercedes':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_mercedess = types.InlineKeyboardMarkup(row_width=1)
        kb_mersf1_power = types.InlineKeyboardButton(text='Mercedes F1 W10 EQ Power+', callback_data='mersf1_power')
        kb_mersf1_w11 = types.InlineKeyboardButton(text='Mercedes-AMG F1 W11 EQ Performance (2020)', callback_data='mersf1_w11')
        kb_mersf1_w12 = types.InlineKeyboardButton(text='Mercedes-AMG F1 W12 E Performance (2021)', callback_data='mersf1_w12')
        kb_mercedess.add(kb_mersf1_power, kb_mersf1_w11, kb_mersf1_w12)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль Mercedes F1', reply_markup=kb_mercedess)


    if call.data == 'mersf1_power':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Mercedes AMG F1 W10 EQ Power+ — гоночный автомобиль с открытыми колёсами в '
                   'Формуле-1, был разработан и построен командой конструктором Mercedes AMG Petronas'
                   ' Motorsport для участия в чемпионате мира Формулы-1 сезона 2019 года. Болид был'
                   ' оснащен двигателем Mercedes 2019 года спецификации, M10 EQ Power+. Пилотировали '
                   'в 2019 году болид британский пилот Льюис Хэмилтон, выступавший в команде седьмой год, '
                   'и финский Валттери Боттас, выступавший за команду третий год.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/power.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'mersf1_w11':
        bot.delete_message(call.message.chat.id, call.message.message_id)

        caption = ('Mercedes-AMG F1 W11 EQ Performance — гоночный автомобиль Формулы-1, спроектированный и построенный командой Mercedes-AMG Petronas F1 под руководством Джеймса Эллисона, Джона Оуэна, Майка Эллиотта, Лоика Серры, Эшли Уэй'
                   ' Эмилиано Джанджулио, Джаррода Мерфи и Эрик Бландин примет'
                   ' участие в чемпионате мира Формулы-1 2020 года. Машиной управляли Льюис Хэмилтон и'
                   ' Валттери Боттас, которые оставались в команде восьмой и четвертый '
                   'сезоны соответственно.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/amg-eq-perfomance.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)



    if call.data == 'mersf1_w12':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Mercedes-AMG F1 W12 E Performance, обычно сокращенно Mercedes W12, — гоночный '
                   'автомобиль Формулы-1, разработанный и построенный командой Mercedes-AMG Petronas '
                   'Formula One под руководством Джеймса Эллисона для участия в чемпионате мира Формулы-1'
                   ' 2021 года. Машиной управляли Льюис Хэмилтон и Валттери Боттас.[2] Автомобиль основан на Mercedes-AMG F1'
                   ' W11 EQ Performance, который выиграл чемпионат пилотов и конструкторов в предыдущем сезоне.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/mers-w12-perfomance.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)




# F E R R A R I




    if call.data == 'ferrari':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_ferrari = types.InlineKeyboardMarkup(row_width=1)
        kb_ferrari_125 = types.InlineKeyboardButton(text='Ferrari 125 F1', callback_data='ferrari_125')
        kb_ferrari_312 = types.InlineKeyboardButton(text='Ferrari 312', callback_data='ferrari_312')
        kb_ferrari_2007 = types.InlineKeyboardButton(text='Ferrari F2007', callback_data='ferrari_f2007')
        kb_ferrari.add(kb_ferrari_2007,kb_ferrari_312, kb_ferrari_125)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль Ferrari F-1', reply_markup=kb_ferrari)

    if call.data == 'ferrari_125':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Компания Ferrari выпустила свой первый гоночный автомобиль с '
                                'открытыми колесами, Ferrari 125 F1, в 1948 году. Автомобиль был р'
                                'азработан Джоакино Коломбо и имел двигатель Ferrari 125 объемом 1,5'
                                ' литра и мощностью 225-280 л.с. при 7500 об./мин. Машина имела пространственную раму,'
                                ' сваренную из стальных труб, двойные рычаги с поперечной листовой рессорой '
                                'на передней подвеске и двойные рычаги с торсионом на задней подвеске. ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/ferrari_125.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption = caption, reply_markup=keyboard)


    if call.data == 'ferrari_312':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Ferrari 312 F1 - это гоночный автомобиль, выпущенный компанией '
                       'Ferrari в 1966-1969 годах для участия в чемпионате Формулы-1. Автомобиль '
                       'имел 3-литровый 12-цилиндровый двигатель, откуда и получил своё название. '
                       'Он был разработан Мауро Форгьери и имел '
                       'полумонококовую алюминиевую раму с трубчатыми стальными рамами на заклёпках.  ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/ferrari_312.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption = caption, reply_markup=keyboard)

    if call.data == 'ferrari_312':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Ferrari 312 F1 - это гоночный автомобиль, выпущенный компанией '
                       'Ferrari в 1966-1969 годах для участия в чемпионате Формулы-1. Автомобиль '
                       'имел 3-литровый 12-цилиндровый двигатель, откуда и получил своё название. '
                       'Он был разработан Мауро Форгьери и имел '
                       'полумонококовую алюминиевую раму с трубчатыми стальными рамами на заклёпках.  ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/ferrari_312.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)




    if call.data == 'ferrari_f2007':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Ferrari F2007 - это болид Формулы-1, построенный для участия в чемпионате 2007 года. '
                       'Болид был презентован 14 января 2007 года и был разработан Альдо Коста и Николасом Томбазисом.'
                       ' Болид оснащен двигателем Ferrari 056 объемом 2,4 литра, V8, атмосферный, мощностью 700 л.с.'
                       ' при 19 000 об./мин. '
                       'Шасси болида выполнено из углеродного волокна и сотовой композитной структуры')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/ferrari_2007.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)




#A S T O N    M A R T I N

    if call.data == 'aston_martin':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_aston = types.InlineKeyboardMarkup(row_width=1)
        kb_aston_dbr_4 = types.InlineKeyboardButton(text='Aston Martin DBR4', callback_data='kb_aston_dbr_4')
        kb_aston_dbr_5 = types.InlineKeyboardButton(text='Aston Martin DBR5', callback_data='kb_aston_dbr_5')
        #kb_ferrari_2007 = types.InlineKeyboardButton(text='Ferrari F2007', callback_data='ferrari_f2007')
        kb_aston.add(kb_aston_dbr_4, kb_aston_dbr_5)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль Aston Martin F1', reply_markup=kb_aston)

    if call.data == 'kb_aston_dbr_4':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Aston Martin DBR4 - это гоночный автомобиль Формулы-1, разработанный Тедом Каттингом'
                   ' для Aston Martin. Он был создан на базе спортивного'
                   ' автомобиля DB3S и дебютировал в чемпионатах мира только в 1959 году на Гран-при'
                   ' Нидерландов. Однако концепция и '
                   'многие технологии гоночной машины оказались устаревшими и не позволили ей '
                   'бороться за высокие места в Гран-при.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/dbr4.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

    if call.data == 'kb_aston_dbr_5':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Aston Martin DBR5 — гоночный автомобиль Формулы-1, разработанный производителем спортивных автомобилей Aston Martin.'
                   'DBR5 должен был быть легче и меньше своего предшественника и, как ожидалось, был быстрее. Однако в сезоне 1960 года'
                   ' ему также не удалось добиться конкурентоспособных результатов, и Aston Martin выбыл из Формулы-1.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/dbr5.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)

#  R  E   D     B U L L
    if call.data == 'red_bull':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        kb_bull = types.InlineKeyboardMarkup(row_width=1)
        kb_bull_rb_6 = types.InlineKeyboardButton(text='Red Bull RB6', callback_data='bull_rb_6')
        kb_bull_rb_9 = types.InlineKeyboardButton(text='Red Bull RB9', callback_data='bull_rb_9')
        kb_bull_rb_15 = types.InlineKeyboardButton(text='Red Bull RB15', callback_data='bull_rb_15')
        kb_bull.add(kb_bull_rb_6, kb_bull_rb_9, kb_bull_rb_15)
        bot.send_message(call.message.chat.id, text='Выберите автомобиль Red  Bull F1', reply_markup=kb_bull)


    if call.data == 'bull_rb_6':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Red Bull RB6 - это гоночный автомобиль с открытыми колесами, разработанный'
                   ' и построенный при помощи Эдриана Ньюи для участия в гонках Формулы-1 сезона 2010.'
                   ' Он был запущен 10 февраля 2010 года в Хересе. Этот автомобиль был ведущим в чемпионате мира Формулы-1'
                   ' 2010 года, и его водитель Себастьян Феттель'
                   ' стал самым молодым в истории Чемпионом мира.')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/redbull_rb6.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'bull_rb_9':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Red Bull RB9 — гоночный автомобиль Формулы-1, разработанный Адрианом Ньюи.'
                   'ашиной управляли (на тот момент) трехкратный чемпион мира среди пилотов Себастьян '
                   'Феттель и его товарищ по команде Марк Уэббер-1.'
                   'Red Bull RB9 был очень успешным болидом в сезоне 2013 года. В течение этого сезона, Red Bull RB9'
                   ' выиграл 13 гонок из 19,'
                   ' занял 24 места на подиуме, а также имел 11 поул-позиций и 12 лучших кругов. ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/redbull_rb_9.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


    if call.data == 'bull_rb_15':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        caption = ('Red Bull RB15 — . Это был гоночный автомобиль, разработанный командой '
                   'Red Bull Racing для участия в Чемпионате мира сезона 2019 года.'
                   'В сезоне 2019 года, Red Bull RB15 выиграл 3 гонки из 21, занял 5 мест на подиуме, а также имел 2 поул-позиции и 5 лучших кругов. ')
        back_button = types.InlineKeyboardButton('Выбрать другую марку', callback_data='back')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(back_button)
        with open('img/redbull_rb15.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=keyboard)


bot.polling(none_stop=True)