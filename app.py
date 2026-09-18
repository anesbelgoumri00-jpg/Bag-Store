
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
import os
import urllib.request
import urllib.parse

app = Flask(__name__)

DB = Path(__file__).with_name("orders.db")


# =========================================================
# TELEGRAM
# =========================================================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "7363392227"


# =========================================================
# معلومات المنتج
# =========================================================

PRODUCT_NAME = "Sacoche Lacoste"
PRODUCT_PRICE = 2500


# =========================================================
# أسعار NOEST
#
# home    = Livraison Domicile
# stopdesk = Livraison Stopdesk
#
# لا نستخدم أسعار Retour
# =========================================================

DELIVERY_PRICES = {

    "Adrar": {
        "home": 1500,
        "stopdesk": 1000
    },

    "Chlef": {
        "home": 800,
        "stopdesk": 500
    },

    "Laghouat": {
        "home": 1000,
        "stopdesk": 600
    },

    "Oum El Bouaghi": {
        "home": 800,
        "stopdesk": 500
    },

    "Batna": {
        "home": 800,
        "stopdesk": 500
    },

    "Béjaïa": {
        "home": 800,
        "stopdesk": 500
    },

    "Biskra": {
        "home": 1000,
        "stopdesk": 600
    },

    "Béchar": {
        "home": 1200,
        "stopdesk": 800
    },

    "Blida": {
        "home": 800,
        "stopdesk": 500
    },

    "Bouira": {
        "home": 800,
        "stopdesk": 500
    },

    "Tamanrasset": {
        "home": 2000,
        "stopdesk": 1500
    },

    "Tébessa": {
        "home": 900,
        "stopdesk": 600
    },

    "Tlemcen": {
        "home": 900,
        "stopdesk": 600
    },

    "Tiaret": {
        "home": 900,
        "stopdesk": 600
    },

    "Tizi Ouzou": {
        "home": 800,
        "stopdesk": 500
    },

    "Alger": {
        "home": 700,
        "stopdesk": 450
    },

    "Djelfa": {
        "home": 1000,
        "stopdesk": 600
    },

    "Jijel": {
        "home": 800,
        "stopdesk": 500
    },

    "Sétif": {
        "home": 750,
        "stopdesk": 450
    },

    "Saïda": {
        "home": 900,
        "stopdesk": 600
    },

    "Skikda": {
        "home": 800,
        "stopdesk": 500
    },

    "Sidi Bel Abbès": {
        "home": 850,
        "stopdesk": 500
    },

    "Annaba": {
        "home": 800,
        "stopdesk": 500
    },

    "Guelma": {
        "home": 900,
        "stopdesk": 600
    },

    "Constantine": {
        "home": 800,
        "stopdesk": 500
    },

    "Médéa": {
        "home": 800,
        "stopdesk": 500
    },

    "Mostaganem": {
        "home": 800,
        "stopdesk": 500
    },

    "M'Sila": {
        "home": 800,
        "stopdesk": 500
    },

    "Mascara": {
        "home": 850,
        "stopdesk": 500
    },

    "Ouargla": {
        "home": 1100,
        "stopdesk": 700
    },

    "Oran": {
        "home": 800,
        "stopdesk": 500
    },

    "El Bayadh": {
        "home": 1200,
        "stopdesk": 800
    },

    "Illizi": {
        "home": 1900,
        "stopdesk": 1500
    },

    "Bordj Bou Arreridj": {
        "home": 600,
        "stopdesk": 400
    },

    "Boumerdès": {
        "home": 800,
        "stopdesk": 500
    },

    "El Tarf": {
        "home": 900,
        "stopdesk": 600
    },

    "Tindouf": {
        "home": 1700,
        "stopdesk": 1000
    },

    "Tissemsilt": {
        "home": 850,
        "stopdesk": 500
    },

    "El Oued": {
        "home": 1100,
        "stopdesk": 700
    },

    "Khenchela": {
        "home": 800,
        "stopdesk": 500
    },

    "Souk Ahras": {
        "home": 900,
        "stopdesk": 600
    },

    "Tipaza": {
        "home": 800,
        "stopdesk": 500
    },

    "Mila": {
        "home": 800,
        "stopdesk": 500
    },

    "Aïn Defla": {
        "home": 800,
        "stopdesk": 500
    },

    "Naâma": {
        "home": 1200,
        "stopdesk": 800
    },

    "Aïn Témouchent": {
        "home": 850,
        "stopdesk": 500
    },

    "Ghardaïa": {
        "home": 1100,
        "stopdesk": 700
    },

    "Relizane": {
        "home": 850,
        "stopdesk": 500
    },

    "Timimoun": {
        "home": 1500,
        "stopdesk": 1000
    },

    "Ouled Djellal": {
        "home": 1000,
        "stopdesk": 600
    },

    "Beni Abbes": {
        "home": 1200,
        "stopdesk": 800
    },

    "In Salah": {
        "home": 1800,
        "stopdesk": 1200
    },

    "Touggourt": {
        "home": 1100,
        "stopdesk": 700
    },

    "Djanet": {
        "home": 2200,
        "stopdesk": 1600
    },

    "El M'Ghair": {
        "home": 1100,
        "stopdesk": 700
    },

    "El Meniaa": {
        "home": 1100,
        "stopdesk": 700
    }
}


# =========================================================
# قاعدة البيانات
# =========================================================

def init_db():

    with sqlite3.connect(DB) as con:

        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                phone TEXT NOT NULL,

                wilaya TEXT NOT NULL,

                commune TEXT NOT NULL,

                product TEXT NOT NULL,

                color TEXT NOT NULL,

                price TEXT NOT NULL,

                delivery_type TEXT,

                delivery_price INTEGER,

                total_price INTEGER,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # قراءة الأعمدة الموجودة
        columns = [
            row[1]
            for row in con.execute(
                "PRAGMA table_info(orders)"
            ).fetchall()
        ]


        # إضافة color إذا كانت قاعدة البيانات قديمة

        if "color" not in columns:

            con.execute("""
                ALTER TABLE orders
                ADD COLUMN color TEXT DEFAULT 'غير محدد'
            """)


        # إضافة نوع التوصيل

        if "delivery_type" not in columns:

            con.execute("""
                ALTER TABLE orders
                ADD COLUMN delivery_type TEXT
            """)


        # إضافة سعر التوصيل

        if "delivery_price" not in columns:

            con.execute("""
                ALTER TABLE orders
                ADD COLUMN delivery_price INTEGER
            """)


        # إضافة السعر الإجمالي

        if "total_price" not in columns:

            con.execute("""
                ALTER TABLE orders
                ADD COLUMN total_price INTEGER
            """)


# =========================================================
# إرسال Telegram
# =========================================================

def send_telegram(message):

    if not TELEGRAM_TOKEN:

        print(
            "❌ TELEGRAM_TOKEN غير موجود "
            "في Environment Variables"
        )

        return


    print("✅ TELEGRAM_TOKEN موجود")


    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )


    data = urllib.parse.urlencode({

        "chat_id": TELEGRAM_CHAT_ID,

        "text": message

    }).encode("utf-8")


    try:

        req = urllib.request.Request(

            url,

            data=data,

            method="POST"

        )


        with urllib.request.urlopen(
            req,
            timeout=10
        ) as response:

            result = response.read().decode(
                "utf-8"
            )

            print(
                "✅ Telegram response:",
                result
            )


    except Exception as e:

        print(
            "❌ Telegram error:",
            repr(e)
        )


# =========================================================
# الصفحة الرئيسية
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    message = None


    if request.method == "POST":

        # ---------------------------------------------
        # معلومات الزبون
        # ---------------------------------------------

        name = request.form.get(
            "name",
            ""
        ).strip()


        phone = request.form.get(
            "phone",
            ""
        ).strip()


        wilaya = request.form.get(
            "wilaya",
            ""
        ).strip()


        commune = request.form.get(
            "commune",
            ""
        ).strip()


        color = request.form.get(
            "color",
            ""
        ).strip()


        # ---------------------------------------------
        # نوع التوصيل
        #
        # home = المنزل
        # stopdesk = المكتب
        # ---------------------------------------------

        delivery_type = request.form.get(
            "delivery_type",
            ""
        ).strip()


        # ---------------------------------------------
        # التحقق من المعلومات
        # ---------------------------------------------

        if not all([
            name,
            phone,
            wilaya,
            commune,
            color
        ]):

            message = (
                "يرجى ملء جميع الخانات "
                "واختيار اللون."
            )


        elif color not in [
            "أزرق",
            "أسود"
        ]:

            message = (
                "اللون المختار غير صحيح."
            )


        elif delivery_type not in [
            "home",
            "stopdesk"
        ]:

            message = (
                "يرجى اختيار نوع التوصيل."
            )


        elif wilaya not in DELIVERY_PRICES:

            message = (
                "لا يوجد سعر توصيل مسجل "
                "لهذه الولاية."
            )


        else:

            # -----------------------------------------
            # استخراج سعر التوصيل
            # -----------------------------------------

            delivery_price = DELIVERY_PRICES[
                wilaya
            ][
                delivery_type
            ]


            # -----------------------------------------
            # حساب المجموع
            # -----------------------------------------

            total_price = (
                PRODUCT_PRICE
                + delivery_price
            )


            # -----------------------------------------
            # اسم نوع التوصيل
            # -----------------------------------------

            if delivery_type == "home":

                delivery_name = "التوصيل إلى المنزل"

            else:

                delivery_name = "التوصيل إلى المكتب (StopDesk)"


            # -----------------------------------------
            # السعر كنص
            # -----------------------------------------

            product_price_text = (
                f"{PRODUCT_PRICE} DA"
            )


            delivery_price_text = (
                f"{delivery_price} DA"
            )


            total_price_text = (
                f"{total_price} DA"
            )


            # -----------------------------------------
            # حفظ الطلب
            # -----------------------------------------

            with sqlite3.connect(DB) as con:

                con.execute(
                    """
                    INSERT INTO orders
                    (
                        name,
                        phone,
                        wilaya,
                        commune,
                        product,
                        color,
                        price,
                        delivery_type,
                        delivery_price,
                        total_price
                    )

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,

                    (
                        name,
                        phone,
                        wilaya,
                        commune,
                        PRODUCT_NAME,
                        color,
                        product_price_text,
                        delivery_type,
                        delivery_price,
                        total_price
                    )
                )


            # -----------------------------------------
            # رسالة Telegram
            # -----------------------------------------

            telegram_message = f"""
🛍️ طلب جديد!

━━━━━━━━━━━━━━

👤 الاسم:
{name}

📞 الهاتف:
{phone}

📍 الولاية:
{wilaya}

🏠 البلدية:
{commune}

━━━━━━━━━━━━━━

👜 المنتج:
{PRODUCT_NAME}

🎨 اللون:
{color}

━━━━━━━━━━━━━━

🚚 نوع التوصيل:
{delivery_name}

💰 سعر المنتج:
{product_price_text}

🚚 سعر التوصيل:
{delivery_price_text}

💵 المجموع:
{total_price_text}

━━━━━━━━━━━━━━
"""


            # -----------------------------------------
            # إرسال الطلب إلى Telegram
            # -----------------------------------------

            send_telegram(
                telegram_message
            )


            # -----------------------------------------
            # الانتقال إلى صفحة النجاح
            # -----------------------------------------

            return redirect(
                url_for("success")
            )


    return render_template(
        "index.html",
        message=message
    )


# =========================================================
# صفحة نجاح الطلب
# =========================================================

@app.route("/success")
def success():

    return render_template(
        "success.html"
    )


# =========================================================
# صفحة Admin
# =========================================================

@app.route("/admin")
def admin():

    with sqlite3.connect(DB) as con:

        orders = con.execute(
            """
            SELECT

                id,

                name,

                phone,

                wilaya,

                commune,

                product,

                color,

                price,

                delivery_type,

                delivery_price,

                total_price,

                created_at

            FROM orders

            ORDER BY id DESC
            """
        ).fetchall()


    return render_template(
        "admin.html",
        orders=orders
    )


# =========================================================
# إنشاء قاعدة البيانات
# =========================================================

init_db()


# =========================================================
# تشغيل التطبيق
# =========================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
