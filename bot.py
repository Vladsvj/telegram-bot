import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict

TOKEN = "7876593451:AAGWOLSyy6tDMJMFKpc5Nddk5WuLlpVkAac"
MANAGER_ID = 7824901075  # Telegram ID менеджера

bot = telebot.TeleBot(TOKEN)

# Хранилище истории экранов для каждого пользователя
user_history = defaultdict(list)

# Главное меню
main_menu = InlineKeyboardMarkup()
main_menu.row(InlineKeyboardButton("📋Трудоустройств|Сотрудничество", callback_data="trud"))
main_menu.row(InlineKeyboardButton("🚖Лицензия такси|Индефикатор", callback_data="flota"))
main_menu.row(InlineKeyboardButton("🚚Прайс оформления документов", callback_data="praca"))
main_menu.row(InlineKeyboardButton("🤝Сотрудничество с автопарками", callback_data="wspolpraca"))
main_menu.row(InlineKeyboardButton("🔧Автосервис", callback_data="servis"))
main_menu.row(InlineKeyboardButton("🚘Аренда авто", callback_data="wynajem"))

# Кнопки "Назад" и "Связаться с менеджером"
def get_extended_menu(section_key):
    safe_key = section_key.replace(" ", "_").replace("📋", "menu").replace("🚖", "taxi").replace("🚚", "delivery").replace("🤝", "partners").replace("🔧", "service").replace("🚘", "rent")
    menu = InlineKeyboardMarkup()
    menu.row(
        InlineKeyboardButton("⬅ Назад", callback_data="back"),
        InlineKeyboardButton("📩 Связаться с менеджером",  url="https://t.me/managerhubpl")
    )
    return menu

# Удаление предыдущего сообщения
def delete_prev_message(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

# Сохраняем предыдущий экран
def save_history(call, menu_key):
    user_history[call.message.chat.id].append(menu_key)

# Обработчик /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "*🚖ПРИВЕТСТВУЮ\\!* \n\n" \
           "Выберите из меню интересующий вас вариант"
    with open("menu_photo.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=main_menu, parse_mode="MarkdownV2")
    user_history[message.chat.id] = []  # Сброс истории при старте

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id

    if call.data == "main":
        delete_prev_message(call)
        with open("menu_photo.jpg", "rb") as photo:
            text = "*🚖ПРИВЕТСТВУЮ\\!* \n\nВыберите из меню интересующий вас вариант"
            bot.send_photo(chat_id, photo, caption=text, reply_markup=main_menu, parse_mode="MarkdownV2")
        user_history[chat_id] = []


    if call.data == "trud":
        save_history(call, "main")
        delete_prev_message(call)
        menu = InlineKeyboardMarkup()
        menu.add(InlineKeyboardButton("🚖 Водитель такси", callback_data="employment_taxi"))
        menu.add(InlineKeyboardButton("📦 Курьер", callback_data="employment_couriers"))
        menu.add(InlineKeyboardButton("🤝 Сотрудничество B2B", callback_data="employment_b2b"))
        menu.add(InlineKeyboardButton("🤝 Разрешение на работу в Польше", callback_data="work_poland"))
        menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back"))
        bot.send_message(chat_id, "📋 Выберите тип трудоустройства", reply_markup=menu)

    if call.data == "wspolpraca":
        save_history(call, "main")
        delete_prev_message(call)
        menu = InlineKeyboardMarkup()
        menu.add(InlineKeyboardButton("Лицензия, партнёр, доход", callback_data="license"))
        menu.add(InlineKeyboardButton("Аренда, пассив, прибыль", callback_data="arenda"))
        menu.add(InlineKeyboardButton("Субаренда", callback_data="subarenda"))
        menu.add(InlineKeyboardButton("⬅ Назад", callback_data="back"))
        bot.send_message(chat_id, "📋 Выберите подходящий вариант:", reply_markup=menu)

    elif call.data == "employment_taxi":
        save_history(call, "trud")
        delete_prev_message(call)
        info = (
            "*Для граждан Украины*\n\n"
            "*Необходимые документы:*\n\n"
            "✅Паспорт\n"
            "✅Польский идентификационный номер (PESEL)\n\n"

            "📌 Если у вас есть международная защита, карта резидента, карта поляка, сталый побыт или диплом польского университета, обязательно возьмите их с собой.\n"
            "📌 Студентам также необходимо предоставить студенческий билет и справку из учебного заведения.\n\n"
            "═════════════════════\n"
            "*Для граждан Беларуси, Грузии, Армении, Молдовы*\n\n"
            "*Необходимые документы:*\n\n"
            "✅Паспорт\n"
            "✅Документ легализации (основанный на работе или учебе)\n"
            "✅Разрешение на работу (оформляется работодателем, срок изготовления – до 10 рабочих дней)\n\n"

            "📌 Если вы уже трудоустроены в другой компании, потребуется подтверждение ежемесячных оплат ZUS и ваш трудовой договор.\n"
            "📌 Если у вас есть международная защита, карта резидента, карта поляка, сталый побыт или диплом польского университета, разрешение на работу не требуется.\n\n"
            "═════════════════════\n"
            "*Для граждан европейских стран*\n\n"
            "*Необходимые документы:*\n\n"
            "✅Паспорт или ID-карта\n"
            "✅Подтверждённая дата въезда в Польшу (Если вы не гражданин Польши)\n\n"

            "📌 Вы можете работать без разрешения на работу до 3 месяцев с момента въезда.\n"
            "📌 Если у вас есть международная защита, карта резидента, карта поляка, сталый побыт или диплом польского университета, разрешение на работу не требуется.\n\n"
            "═════════════════════\n"
            "*Для граждан Узбекистана, Азербайджана, Туркменистана, Турции и других стран*\n\n"
            "*Необходимые документы:*\n\n"
            "✅Паспорт\n"
            "✅Польские водительские права\n"
            "✅Документ, подтверждающий вашу легализацию (основанный на работе или учебе)\n"
            "✅Разрешение на работу (оформляется работодателем, срок изготовления 3–6 месяцев)\n\n"

            "📌 Если вы уже трудоустроены в другой компании, потребуется подтверждение ежемесячных оплат ZUS и ваш трудовой договор.\n"
            "📌 Если у вас есть международная защита, карта резидента, карта поляка, сталый побыт или диплом польского университета, разрешение на работу не требуется.\n\n"
        )
        bot.send_message(chat_id, info, reply_markup=get_extended_menu("Водитель такси"), parse_mode="Markdown")

    elif call.data == "employment_couriers":
        save_history(call, "trud")
        delete_prev_message(call)
        text = "📦Раздел скоро появится"
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Курьер"), parse_mode="Markdown")

    elif call.data == "employment_b2b":
        save_history(call, "trud")
        delete_prev_message(call)
        text = (
            "📦 *Чтобы работать с нами по B2B-договору, вам необходимо:*\n\n"
            "✅Предоставить данные вашей компании.\n"
            "✅Подписать договор с нами.\n\n"
            "📌 *Важно!* Ваша фирма должна иметь открытый код PKD:\n"
            "49.31.Z или 49.39.Z (по рекомендации вашего бухгалтера)\n\n"

            "*Готовы к сотрудничеству? Свяжитесь с нами! 🚀*\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Сотрудничество B2B"), parse_mode="Markdown")

    elif call.data == "work_poland":
        save_history(call, "trud")
        delete_prev_message(call)
        text = (
            "*Для граждан Беларуси, Молдовы, Армении, Грузии*\n\n"
            "⏳ Срок изготовления: до 10 рабочих дней.\n"
            "📆 Срок действия: 2 года.\n"
            "✅Позволяет официально трудоустроиться в Польше и оформить визу.\n\n"

            "*📌 Необходимые документы:*\n"
            "✅Скан всех заполненных страниц паспорта (разворот)\n"
            "✅Скан польских водительских прав (обе стороны)\n"
            "✅Оплата\n\n"
            "═════════════════════\n"
            "*Для граждан Азербайджана, Туркменистана, Узбекистана, Турции и других стран, не входящих в ЕС*\n\n"

            "⏳ Срок изготовления: 3–6 месяцев\n"
            "📆 Срок действия: 1 год\n"
            "✅ Позволяет официально трудоустроиться в Польше и оформить визу.\n\n"

            "*📌 Необходимые документы:*\n"
            "✅Скан всех заполненных страниц паспорта (разворот)\n"
            "✅Оплата\n"
            "✅Документ из уженда, подтверждающий, что на данную вакансию не претендует польский гражданин (оформляет работодатель).\n"
            "(Из-за последнего документа срок ожидания увеличивается.)\n\n"
            "═════════════════════\n"
            "*Для граждан Украины*\n"
            "В связи с войной разрешение на работу не требуется.\n\n"

            "*📌 Готовы оформить документы? Свяжитесь с нашим консультантом! 🚀*\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Разрешение на работу в Польше"), parse_mode="Markdown")

    elif call.data == "flota":
        save_history(call, "main")
        delete_prev_message(call)
        text = (
            "*Чтобы начать работать в такси, необходимо получить Идентификатор (лицензию для водителя).\n"
            "Для этого вам нужно собрать несколько документов и принести их в наш офис для подачи. Вот полный список:*\n\n"
            "✅Справка о несудимости из вашей страны и её присяжный перевод. Перевод можно заказать в фирме, зарегистрированной в Польше. (Обратите внимание: если вы находитесь в Польше по международной защите, Карте Поляка или имеете сталый побыт, справка о несудимости из вашей страны не требуется.)\n"
            "✅Справка о несудимости в Польше.\n"
            "✅Медицинская справка для работы в такси\n"
            "✅Справка от психиатра для работы в такси.\n"
            "✅Польские водительские права.\n"
            "✅Фотография 3,5х4,5 см.\n"
            "✅Документы легализации для всех граждан, кроме Украины.\n\n"

            "*Мы поможем вам с оформлением и подачей документов, чтобы вы могли как можно быстрее начать работать!*\n\n"
            "═════════════════════\n"
            "*Документы для автомобиля*\n\n"
            "Чтобы зарегистрировать автомобиль для работы в такси, необходимы следующие документы:\n"
            "✅Техпаспорт с печатью такси и актуальным техосмотром.\n"
            "✅Документ-соглашение о разрешении использования авто в такси (оформляется в нашем офисе).\n"
            "✅Договор лизинга с разрешением на субаренду и использование авто в такси (для лизинговых автомобилей).\n\n"

            "⏳ Оформление выписа из лицензии занимает 3–6 месяцев.\n"
            "🚫 Машина без выписа не может работать в такси.\n\n"
            "═════════════════════\n"
            "*⚡ Хотите начать работать сразу?*\n"
            "*У нас можно приобрести готовый выпис и выйти на линию всего за 2–3 дня!*\n"
            "*📌 Количество выписов ограничено, уточняйте у консультанта.*\n\n"

            "*Отправьте менеджеру слово (hub+3) и уже на третий день вы начнете зарабатывать!*\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Лицензия такси|Индефикатор"), parse_mode="Markdown")

    elif call.data == "praca":
        save_history(call, "main")
        delete_prev_message(call)
        text = (
            "*Стоимость оформления документов*\n"
            "✅ Идентификатор (лицензия для водителя) – БЕСПЛАТНО\n"
            "✅ Справка о несудимости (Польша):\n"
            "🔹 Если оформляем мы – 70 PLN\n"
            "🔹 Если оформляете самостоятельно – 30 PLN\n\n"

            "✅ Польские водительские права (с нашим сопровождением)\n"
            "🔹 При наличии всех документов – 300 PLN\n\n"

            "✅ Выпис из лицензии:\n"
            "🔹 Обычное оформление (3–6 месяцев) – 50 PLN\n"
            "🔹 Срочное оформление (1–3 дня) – 350 PLN (количество ограничено!)\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Стоимость оформления"), parse_mode="Markdown")

    elif call.data == "license":
        save_history(call, "wspolpraca")
        delete_prev_message(call)
        info = (
            "*Выпис из лицензии на авто*\n"
            "🔹 Техпаспорт с печатью такси и актуальным техосмотром\n"
            "🔹 Договор на использование авто в такси (оформляется в нашем офисе между нашей фирмой и владельцем автомобиля)\n"
            "🔹 Скан лизингового договора (для лизинговых авто) – должен содержать разрешение на использование машины в такси и сдачу в аренду.\n\n"

            "💰 Стоимость выписа зависит от условий сотрудничества и обсуждается с руководством.\n"
            "📌 Оформите выпис и начните зарабатывать уже в ближайшие дни! 🚖\n\n"
        )
        bot.send_message(chat_id, info, reply_markup=get_extended_menu("Лицензия, партнер, доход"), parse_mode="Markdown")

    elif call.data == "arenda":
        save_history(call, "wspolpraca")
        delete_prev_message(call)
        text = (
            "*Хотите сдать авто в аренду напрямую нам и не искать водителей самостоятельно?*\n"
            "✅ Бесплатные выписы на авто\n"
            "✅ Официальный договор аренды между владельцем авто и нашей фирмой\n"
            "✅ Гарантированные выплаты\n\n"

            "📌 Все условия обговариваются индивидуально с руководством. Свяжитесь с нами для деталей! 🚖\n\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Аренда, пассив, прибыль"), parse_mode="Markdown")

    elif call.data == "subarenda":
        save_history(call, "wspolpraca")
        delete_prev_message(call)
        text = (
            "*Переживаете, что водитель может не выплатить аренду вовремя?*\n"
            "*Мы предлагаем договор субаренды, который подписывается между:*\n"
            "✅ Фирмой\n"
            "✅ Владельцем авто\n"
            "✅ Водителем\n"
            "🔹 Фиксированная стоимость аренды\n"
            "🔹 Гарантированные выплаты владельцу авто\n"
            "🔹 Фирма берет на себя ответственность за оплату аренды\n\n"

            "📌 Все условия обговариваются индивидуально с руководством. Свяжитесь с нами для деталей! 🚖\n\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Субаренда"), parse_mode="Markdown")

    elif call.data == "servis":
        save_history(call, "main")
        delete_prev_message(call)
        text = (
            "*🔧Регулярное обслуживание*\n"
            "✅Поддерживайте свой автомобиль в отличном состоянии с нашим регулярным техническим обслуживанием\n\n"
            "═════════════════════\n"
            "*🔧Ремонт*\n"
            "✅Профессиональный ремонт для всех марок и моделей автомобилей\n\n"
            "═════════════════════\n"
            "*🔧Шиномонтаж*\n"
            "✅Замена, ротация и балансировка шин\n\n"
            "═════════════════════\n"
            "*🔧Замена запчастей*\n"
            "✅Качественные запчасти по конкурентным ценам\n\n"
        )
        bot.send_message(chat_id, text, reply_markup=get_extended_menu("Автосервис"), parse_mode="Markdown")

    elif call.data == "wynajem":
        save_history(call, "main")
        delete_prev_message(call)
        info = "🚘 У нас вы можете арендовать авто для работы в такси или доставки. Все машины обслужены и застрахованы. Условия обсуждаются индивидуально."
        bot.send_message(chat_id, info, reply_markup=get_extended_menu("Аренда авто"), parse_mode="Markdown")

    elif call.data.startswith("contact_"):
        delete_prev_message(call)
        section = call.data.split("_", 1)[1].replace("_", " ")
        user = call.from_user
        msg_to_manager = f"📩 Пользователь @{user.username or user.first_name} (ID: {user.id}) хочет связаться из раздела: *{section}*"
        bot.send_message(MANAGER_ID, msg_to_manager, parse_mode="Markdown")
        bot.send_message(chat_id, "Менеджер получил ваш запрос. Напишите ему напрямую: https://t.me/managerhubpl")

    elif call.data == "back":
        delete_prev_message(call)
        if user_history[chat_id]:
            previous = user_history[chat_id].pop()
            fake_call = call
            fake_call.data = previous
            callback_query(fake_call)
        else:
            # Вернуться на главный экран с фото
            fake_call = call
            fake_call.data = "main"
            callback_query(fake_call)


# Запуск бота
bot.polling(none_stop=True)
