from .models import Log, User
from .Buttons import *
from .Globals import TEXTS
from tg.models import *


def start(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()

    if not tglog:
        tglog = Log()
        tglog.user_id = user.id
        tglog.message = {"state": 0}
        tglog.save()
    log = tglog.messages
    print("a")

    tg_user = User.objects.filter(user_id=user.id).first()

    if not tg_user:
        tg_user = User()
        tg_user.user_id = user.id
        tg_user.username = user.username
        tg_user.save()
        log['state'] = 0
        print("aaa")

    tglog.messages = log
    tglog.save()
    print("aaaaa")

    if not tg_user.lang:
        update.message.reply_text(TEXTS['START'], reply_markup=btns('lang'))
        print("a1234")

    else:
        if log.get('state', 0) >= 10:
            update.message.reply_text(TEXTS["BOSH_MENU"][tg_user.lang], reply_markup=btns('menu', lang=tg_user.lang))
            log['state'] = 10
            tglog.messages = log
            tglog.save()

        else:
            print(tg_user.phone, tg_user.lang)
            if not tg_user.phone or not tg_user.lang:
                log['state'] = 0
                print("aaa")

                tglog.messages = log
                tglog.save()
                update.message.reply_text(TEXTS['START'], reply_markup=btns('lang'))

            else:
                update.message.reply_text(TEXTS["BOSH_MENU"][tg_user.lang], reply_markup=btns('menu', lang=tg_user.lang))


def message_handler(update, context):
    user = update.message.from_user

    tg_user = User.objects.get(user_id=user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    msg = update.message.text
    log = tglog.messages
    state = log.get('state', 0)

    if state == 0:
        log['state'] = 1
        if msg == "🇺🇿Uz":
            tg_user.lang = 1
            tg_user.save()
        elif msg == "🇷🇺Ru":
            print("A")
            tg_user.lang = 2
            tg_user.save()
        else:
            update.message.reply_text(TEXTS['START'], reply_markup=btns("lang"))
            return 0
        update.message.reply_text(TEXTS["CONTACT"][tg_user.lang], reply_markup=btns('contact', lang=tg_user.lang))
        tglog.messages = log
        tglog.save()
        return 0

    if msg == TEXTS['BACK'][1] or msg == TEXTS['BACK'][2]:
        pass

    elif log['state'] == 1:
        update.message.reply_text(TEXTS["CONTACT2"][tg_user.lang])

    elif log['state'] == 11:
        log['state'] = 12
        update.message.reply_text(TEXTS['BOSH_MENU'], reply_markup=btns('menu'))
        print("qwerty")

    if msg == TEXTS['BTN_MENU'][1] or msg == TEXTS['BTN_MENU'][2]:
        log['state'] = 13
        update.message.reply_text(TEXTS["Bosh Menu 👇"][tg_user.lang], reply_markup=btns('ctgs', lang=tg_user.lang))

    elif log['state'] == 13:
        log['state'] = 14
        log['ctg'] = msg
        l = "uz" if tg_user.lang == 1 else "ru"
        d = {
            f"name_{l}": msg
        }
        ctg = Category.objects.filter(**d).first()
        print(d, ctg)
        if not ctg:
            update.message.reply_text(TEXTS['ERROR'][tg_user.lang])
            return 0
        update.message.reply_text(TEXTS["Bosh Menu 👇"][tg_user.lang], reply_markup=btns('sub', ctg=ctg, lang=tg_user.lang))

    elif log['state'] == 14:
        log['state'] = 15
        log['sub'] = msg
        l = "uz" if tg_user.lang == 1 else "ru"
        d = {
            f"name_{l}": msg
        }
        subctg = SubCategory.objects.filter(**d).first()
        if not subctg:
            update.message.reply_text(TEXTS['ERROR'][tg_user.lang])
            return 0
        update.message.reply_text(TEXTS["Bosh Menu 👇"][tg_user.lang], reply_markup=btns('made_in', subctg=subctg, lang=tg_user.lang))

    elif log['state'] == 15:
        log['state'] = 16
        log['made_in'] = msg
        l = "uz" if tg_user.lang == 1 else "ru"
        d = {
            f"name_{l}": msg
        }
        made = Made_in1.objects.filter(**d).first()
        if not made:
            update.message.reply_text(TEXTS['ERROR'][tg_user.lang])
            return 0

        update.message.reply_text("Quydagilardan birini tanlang", reply_markup=btns(type='product', made_in=msg, lang=tg_user.lang))

    elif log['state'] == 16:
        log['state'] = 16
        log['product'] = msg
        log["nta"] = 1
        l = "uz" if tg_user.lang == 1 else "ru"
        d = {
            f"name_{l}": msg,
        }
        product = Product.objects.filter(**d).first()
        update.message.reply_text("Quyidagilardan birini tanlang. ", reply_markup=btns("prod"))

        print(product)
        Name = f"Name: {getattr(product, f'name_{l}')}\n" if getattr(product, f'name_{l}') else ""
        Made_in = f"Made_in: {product.made_in}\n" if product.made_in else ""
        Description = f"Description: {getattr(product, f'description_{l}')}\n" if getattr(product,
                                                                                          f'description_{l}') else ""

        context.bot.send_photo(
            photo=open(f'{product.img.path}', 'rb'),
            caption=f"{Name}{Made_in}{Description}",
            chat_id=user.id,
            reply_markup=inline_btns('prod', nta=log['nta'])
        )

    elif msg == "📥 Savat":
        log['state'] = 30
        savat = Savat.objects.filter(user_id=user.id)
        s = "Savatda:\n"
        summa = 0
        for i in savat:
            s += f"{i.amount} ✅ {i.product} {i.summ} \n"
            summa += i.summ
        if summa == 0:
            update.message.reply_text("Savatingiz bo'sh")
        else:
            s += f"Maxsulotlar: {summa} so'm\nYetkazip berish: Shahar ichida bepul"

            update.message.reply_text(s, reply_markup=inline_btns("savat", user_id=user.id))
            update.message.reply_text(TEXTS["Bosh Menu 👇"][tg_user.lang], reply_markup=btns('menu', lang=tg_user.lang))

    tglog.messages = log
    tglog.save()


def contact_handler(update, context):
    contact = update.message.contact
    user = update.message.from_user
    tg_user = User.objects.get(user_id=user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages

    print(log)
    if log['state'] == 1:
        tg_user.phone = contact.phone_number
        tg_user.save()
        log.clear()

        log["state"] = 10
        update.message.reply_text(TEXTS["BOSH_MENU"][tg_user.lang], reply_markup=btns('menu', lang=tg_user.lang))

    tglog.messages = log
    tglog.save()


def callback_handler(update, context, kwargs=None):
    query = update.callback_query
    data = query.data
    user = query.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = User.objects.filter(user_id=user.id).first()
    log = tglog.messages

    print(data)
    if data == "+":
        log['nta'] = log.get("nta", 1) + 1
        update.callback_query.answer(f"{log['nta']}")
        query.edit_message_reply_markup(reply_markup=inline_btns("prod", nta=log['nta']))

    elif data == "-":
        if log.get("nta", 1) <= 1:
            pass
        else:
            log['nta'] = log.get("nta", 1) - 1
            update.callback_query.answer(f"{log['nta']}")
            query.edit_message_reply_markup(reply_markup=inline_btns("prod", nta=log['nta']))

    elif data == "savat":
        savat = Savat.objects.filter(product=log['product'], user_id=user.id).first()
        if savat:
            savat.amount = savat.amount + log['nta']
            savat.summ = int(log['price'].strip("so'm").replace(" ", "")) * savat.amount
            savat.save()
        else:
            savat = Savat()
            savat.amount = log['nta']
            savat.product = log['product']
            savat.priceproduct = log['price']
            savat.user_id = user.id
            print(log)
            savat.summ = int(log['price'].strip("so'm").replace(" ", "")) * log['nta']
            savat.save()
        update.callback_query.answer(f"savatga qo'shildi")
        query.message.delete()

    if log['state'] == 30:
        if data == "🧹 Savatni tozalash":
            Savat.objects.filter(user_id=user.id).delete()
            update.callback_query.answer("Savat tozalandi")
            query.message.delete()
        elif data == "⏰ Yetkazib berish vaqti":
            query.message.reply_text(
                "Sizning buyurtmangiz kun davomida yetkazib beriladi aloqada bo'ling kuryermiz siz bilan tez orada bog'landa 😊")
            query.message.delete()
        elif data == "🚕 Buyurtma berish":
            query.message.reply_text(
                f"{user.username} sizning buyurtmangiz qabul qilindi. Qisqa vaqt ichida kuryerimz siz bilan bog'lanadi 😊")
            query.message.delete()
        elif data == "◀️Orqaga":
            log['state'] = 10
            query.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu', lang=tg_user.lang))
            query.message.delete()
        else:
            Savat.objects.filter(slug=data, user_id=user.id).delete()
            update.callback_query.answer("Savat tozalandi")
            query.message.delete()
            log['state'] = 30
            savat = Savat.objects.filter(user_id=user.id)
            s = "Savatda:\n"
            summa = 0
            for i in savat:
                s += f"{i.amount} ✅ {i.product} {i.summ} \n"
                summa += i.summ
            if summa == 0:
                query.message.reply_text("Savatingiz bo'sh")
            else:
                s += f"Maxsulotlar: {summa} so'm\nYetkazip berish: Shahar ichida bepul"

                query.message.reply_text(s, reply_markup=inline_btns("savat", user_id=user.id))

    tglog.messages = log
    tglog.save()
