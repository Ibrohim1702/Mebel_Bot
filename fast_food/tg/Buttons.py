from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from tg.Globals import *
from tg.models import *


def btns(type=None, ctg=None, ctgs=None, subctg=None, lang=1, made_in=True):
    btn = []
    if type == "menu":
        btn = [
            [KeyboardButton(TEXTS['BTN_MENU'][lang])],
            [KeyboardButton(TEXTS['BTN_MENU1'][lang]), KeyboardButton(TEXTS['BTN_MENU2'][lang])],
        ]

    elif type == 'contact':
        btn = [
            [KeyboardButton(TEXTS['PHONE_CONTACT'][lang], request_contact=True)]
        ]

    elif type == "ctgs":
        btn = []
        ctgs = Category.objects.all()

        for i in range(1, len(ctgs), 2):
            btn1 = ctgs[i - 1].name_uz if lang == 1 else ctgs[i - 1].name_ru
            btn2 = ctgs[i].name_uz if lang == 1 else ctgs[i].name_ru
            btn.append([
                KeyboardButton(btn1), KeyboardButton(btn2)
            ])
        if len(ctgs) % 2:
            btn1 = ctgs[len(ctgs) - 1].name_uz if lang == 1 else ctgs[len(ctgs) - 1].name_ru
            btn.append([KeyboardButton(btn1)])
        btn.append([KeyboardButton(TEXTS['BACK'][lang])])

    elif type == "sub":
        btn = []
        course = SubCategory.objects.filter(ctg=ctg)
        if not course:
            return []
        for i in range(1, len(course), 2):
            btn1 = course[i - 1].name_uz if lang == 1 else course[i - 1].name_ru
            btn2 = course[i].name_uz if lang == 1 else course[i].name_ru
            btn.append([
                KeyboardButton(btn1), KeyboardButton(btn2)
            ])
        if len(course) % 2:
            btn1 = course[len(course) - 1].name_uz if lang == 1 else course[len(course) - 1].name_ru
            btn.append([KeyboardButton(btn1)])
        btn.append([KeyboardButton(TEXTS['BACK'][lang])])

    elif type == "made_in":
        btn = []

        made = Made_in1.objects.filter(subctg=subctg)
        if not made:
            return []
        for i in range(1, len(made), 2):
            btn1 = made[i - 1].name_uz if lang == 1 else made[i - 1].name_ru
            btn2 = made[i].name_uz if lang == 1 else made[i].name_ru
            btn.append([
                KeyboardButton(btn1), KeyboardButton(btn2)
            ])
        if len(made) % 2:
            btn1 = made[len(made) - 1].name_uz if lang == 1 else made[len(made) - 1].name_ru
            btn.append([KeyboardButton(btn1)])
        btn.append([KeyboardButton(TEXTS['BACK'][lang])])

    elif type == "product":
        btn = []
        lan = 'uz' if lang == 1 else 'ru'
        filter = {
            f'name_{lan}': made_in
        }
        made = Made_in1.objects.filter(**filter).first()
        print(">>>>",filter)

        products = Product.objects.filter(made_in=made)

        for i in range(1, len(products), 2):
            btn1 = products[i - 1].name_uz if lang == 1 else products[i - 1].name_ru
            btn2 = products[i].name_uz if lang == 1 else products[i].name_ru
            btn.append([
                KeyboardButton(btn1), KeyboardButton(btn2)
            ])
        if len(products) % 2:
            btn1 = products[len(products) - 1].name_uz if lang == 1 else products[len(products) - 1].name_ru
            btn.append([KeyboardButton(btn1)])
        btn.append([KeyboardButton(TEXTS['BACK'][lang])])

    elif type == "lang":
        btn = [
            [KeyboardButton("🇺🇿Uz"), KeyboardButton("🇷🇺Ru")]
        ]

    # else:
    #     btn = [
    #         [KeyboardButton("🇺🇿Uz"), KeyboardButton("🇷🇺Ru")]
    #     ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def inline_btns(type=None, nta=1, user_id=0):
    btn = []
    if type == "prod":
        btn.append([
            InlineKeyboardButton("-", callback_data="-"),
            InlineKeyboardButton(f"{nta}", callback_data=f"{nta}"),
            InlineKeyboardButton("+", callback_data="+"),
        ])
        btn.append([
            InlineKeyboardButton("📥 Savatga qo'shish", callback_data="savat"),
        ])
    elif type == "savat":
        btn.append([
            InlineKeyboardButton("◀️Orqaga", callback_data="◀️Orqaga"),
            InlineKeyboardButton("🚕 Buyurtma berish", callback_data="🚕 Buyurtma berish")
        ])
        btn.append([
            InlineKeyboardButton("⏰ Yetkazib berish vaqti", callback_data="⏰ Yetkazib berish vaqti"),
        ])
        savat = Savat.objects.filter(user_id=user_id)
        if not savat:
            return InlineKeyboardMarkup([])
        for i in range(len(savat)):
            btn.append([
                InlineKeyboardButton(f"❌{savat[i].product}", callback_data=f"{savat[i].slug}")
            ])
        btn.append([

            InlineKeyboardButton("🧹 Savatni tozalash", callback_data="🧹 Savatni tozalash")
        ])

    return InlineKeyboardMarkup(btn)