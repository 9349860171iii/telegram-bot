import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIG ---
BOT_TOKEN = os.getenv("8609541625:AAHxJC-r6GwmS3uhsBlf3O5yjwjXQm3jMow")
ADMIN_ID = 7286525252

PRODUCTS = {
    "1": {
        "name": "FF Skin Tool Pro",
        "price": "150 BDT",
        "link": "https://example.com/download/ff-tool",
        "details": "এটি একটি প্রিমিয়াম স্কিন টুল।"
    },
    "2": {
        "name": "FreeFire No Recoil Config",
        "price": "200 BDT",
        "link": "https://example.com/download/pubg-config",
        "details": "নো রিকয়েল ফাইল।"
    },
    "3": {
        "name": "Netflix 1 Month Profile",
        "price": "350 BDT",
        "link": "Login: user@mail.com | Pass: 12345",
        "details": "১ মাস প্রিমিয়াম।"
    },
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 পণ্য দেখুন", callback_data='view_products')],
        [InlineKeyboardButton("📞 Support", url="https://t.me/ibrahim05ak")]
    ]
    await update.message.reply_text("🔥 Welcome to Store Bot", reply_markup=InlineKeyboardMarkup(keyboard))

async def product_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    keyboard = []
    for pid, p in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"buy_{pid}")])

    await q.edit_message_text("🛍️ Select Product:", reply_markup=InlineKeyboardMarkup(keyboard))

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    pid = q.data.split("_")[1]
    context.user_data["pid"] = pid
    p = PRODUCTS[pid]

    await q.edit_message_text(
        f"💳 Payment:\n\nbKash: 01XXXXXXXXX\nAmount: {p['price']}\n\n👉 TXID পাঠাও"
    )

async def trx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "pid" not in context.user_data:
        return

    pid = context.user_data["pid"]
    user = update.message.from_user
    txid = update.message.text
    p = PRODUCTS[pid]

    keyboard = [[
        InlineKeyboardButton("✅ Confirm", callback_data=f"ok_{user.id}_{pid}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"no_{user.id}")
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New Order\nUser: {user.id}\nTXID: {txid}\nProduct: {p['name']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text("⏳ Waiting for admin...")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data.split("_")

    if data[0] == "ok":
        uid = int(data[1])
        pid = data[2]

        await context.bot.send_message(
            chat_id=uid,
            text="🎉 Approved!\n" + PRODUCTS[pid]["link"]
        )
        await q.edit_message_text("Approved")

    else:
        uid = int(data[1])
        await context.bot.send_message(chat_id=uid, text="❌ Rejected")
        await q.edit_message_text("Rejected")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(product_menu, pattern="view_products"))
    app.add_handler(CallbackQueryHandler(buy, pattern="buy_"))
    app.add_handler(CallbackQueryHandler(admin, pattern="^(ok|no)_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, trx))

    app.run_polling()

if __name__ == "__main__":
    main()
