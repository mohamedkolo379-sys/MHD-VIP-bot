import os, json
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

TOKEN = "8935590470:AAGJCwz6vlj35nbJGBVIZf6uXKihjWxCgJI"
ADMIN_ID = 8706012170
CODE = "#MHD#ViP#bot#"
NUM_WAVE = "0500269204"
NUM_MOMO = "0500269204"

NOM, PRENOM, NUMERO, IDWIN, CODE_ETAPE = range(5)

def load(f):
    if not os.path.exists(f):
        return [] if f=="gratuit.json" else {}
    try:
        return json.load(open(f, 'r', encoding='utf-8'))
    except:
        return [] if f=="gratuit.json" else {}

def save(f,d):
    json.dump(d, open(f,'w', encoding='utf-8'), indent=2)

async def envoyer_menu_vip(chat_id, context):
    text = "✅ Vérification réussie !\n🔥 MHD VIP 8000F débloqué"
    keyboard = [[InlineKeyboardButton("💣 Mines", callback_data='mines')], [InlineKeyboardButton("✈️ Aviator", callback_data='aviator')], [InlineKeyboardButton("🚀 Lucky Jet", callback_data='lucky')], [InlineKeyboardButton("💥 New Mines", callback_data='new_mines')]]
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update, context):
    await update.message.reply_text("🔥 MHD VIP 8000F - Envoie ton NOM:")
    return NOM

async def get_nom(u,c):
    c.user_data['nom']=u.message.text
    await u.message.reply_text("PRENOM:")
    return PRENOM
async def get_prenom(u,c):
    c.user_data['prenom']=u.message.text
    await u.message.reply_text("NUMERO WHATSAPP:")
    return NUMERO
async def get_num(u,c):
    c.user_data['numero']=u.message.text
    await u.message.reply_text("ID 1WIN:")
    return IDWIN
async def get_idwin(u,c):
    c.user_data['id_1win']=u.message.text
    await u.message.reply_text(f"💳 PAIEMENT 8000F\nWAVE: {NUM_WAVE}\nMoMo: {NUM_MOMO}\nCode: {CODE}")
    return CODE_ETAPE
async def get_code(update, context):
    if update.message.text.strip() != CODE:
        await update.message.reply_text("❌ Mauvais code")
        return CODE_ETAPE
    users = load("users.json")
    uid = str(update.effective_user.id)
    users[uid] = {"nom": context.user_data['nom'], "date": datetime.now().strftime("%d/%m")}
    save("users.json", users)
    await envoyer_menu_vip(update.effective_user.id, context)
    return ConversationHandler.END

async def jeu(update, context):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(f"Signal {q.data}")

app = Application.builder().token(TOKEN).build()
conv = ConversationHandler(entry_points=[CommandHandler("start", start)], states={NOM:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_nom)], PRENOM:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_prenom)], NUMERO:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_num)], IDWIN:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_idwin)], CODE_ETAPE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_code)]}, fallbacks=[])
app.add_handler(conv)
app.add_handler(CallbackQueryHandler(jeu))
app.run_polling()
