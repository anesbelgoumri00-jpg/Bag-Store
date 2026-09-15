
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
import os
import urllib.request
import urllib.parse

app = Flask(__name__)

DB = Path(__file__).with_name("orders.db")

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "7363392227"


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
                price TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def send_telegram(message):

    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN غير موجود في Environment Variables")
        return

    print("✅ TELEGRAM_TOKEN موجود")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

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

        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode("utf-8")
            print("✅ Telegram response:", result)

    except Exception as e:
        print("❌ Telegram error:", repr(e))


@app.route("/", methods=["GET", "POST"])
def index():

    message = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        wilaya = request.form.get("wilaya", "").strip()
        commune = request.form.get("commune", "").strip()

        product = "Sacoche Lacoste"
        price = "2500 DA"

        if not all([name, phone, wilaya, commune]):

            message = "يرجى ملء جميع الخانات."

        else:

            with sqlite3.connect(DB) as con:

                con.execute(
                    """
                    INSERT INTO orders
                    (name, phone, wilaya, commune, product, price)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        phone,
                        wilaya,
                        commune,
                        product,
                        price
                    )
                )

            telegram_message = f"""
🛍️ طلب جديد!

👤 الاسم: {name}
📞 الهاتف: {phone}

📍 الولاية: {wilaya}
🏠 البلدية: {commune}

👜 المنتج: {product}
💰 السعر: {price}
"""

            send_telegram(telegram_message)

            return redirect(url_for("success"))

    return render_template(
        "index.html",
        message=message
    )


@app.route("/success")
def success():
    return render_template("success.html")


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
                price,
                created_at
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

    return render_template(
        "admin.html",
        orders=orders
    )


# إنشاء قاعدة البيانات عند تشغيل التطبيق
init_db()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
