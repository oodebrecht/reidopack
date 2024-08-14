import qrcode
import io
import pyperclip
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Definir produtos e preços com base nas chaves PIX fornecidas
produtos = {
    "produto_1": {"nome": "Acesso VIP Incestos Reais", "preco": "R$ 38,80", "pix_chave": "00020126440014br.gov.bcb.pix0122afjoaninha11@gmail.com520400005303986540538.805802BR5922FUSION VENDAS DIGITAIS6009SAO PAULO62070503***6304DAD0"},
    "produto_2": {"nome": "Acesso VIP Novinhas Vazadas", "preco": "R$ 50,00", "pix_chave": "00020126440014br.gov.bcb.pix0122afjoaninha11@gmail.com520400005303986540550.005802BR5922FUSION VENDAS DIGITAIS6009SAO PAULO62070503***6304A58E"},
    "produto_3": {"nome": "Acesso VIP Fetiches Pesados", "preco": "R$ 38,80", "pix_chave": "00020126440014br.gov.bcb.pix0122afjoaninha11@gmail.com520400005303986540538.805802BR5922FUSION VENDAS DIGITAIS6009SAO PAULO62070503***6304DAD0"},
    "produto_4": {"nome": "Acesso VIP Onlyfans e Privacy", "preco": "R$ 29,90", "pix_chave": "00020126440014br.gov.bcb.pix0122afjoaninha11@gmail.com520400005303986540529.905802BR5922FUSION VENDAS DIGITAIS6009SAO PAULO62070503***630407ED"},
    "produto_5": {"nome": "Tudo Incluso + Lives", "preco": "R$ 149,99", "pix_chave": "00020126440014br.gov.bcb.pix0122afjoaninha11@gmail.com5204000053039865406149.995802BR5922FUSION VENDAS DIGITAIS6009SAO PAULO62070503***63047D27"}
}

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton(f"{produto['nome']} - {produto['preco']}", callback_data=produto_key)]
        for produto_key, produto in produtos.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 Bem-vindo ao nosso serviço VIP! 🎉\n\nEscolha um dos produtos abaixo para continuar:",
        reply_markup=reply_markup
    )

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    produto_key = query.data
    produto = produtos.get(produto_key)
    
    if produto is None:
        await query.message.reply_text("🚫 Produto não encontrado.")
        return

    # Enviar mensagem de confirmação do produto
    await query.message.reply_text(
        f"✅ Você escolheu: {produto['nome']}\n"
        f"💲 Valor: {produto['preco']}\n\n"
        f"Estamos gerando o QR Code e a chave PIX para você. Por favor, aguarde um momento!"
    )

    # Gerar QR code
    qr = qrcode.QRCode()
    qr.add_data(produto["pix_chave"])
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    qr_bytes = io.BytesIO()
    img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)
    
    # Enviar QR code
    await query.message.reply_photo(
        photo=qr_bytes, 
        caption=(
            f"📸 Aqui está o seu QR Code!\n\n"
            f"👉 Produto: {produto['nome']}\n"
            f"💰 Valor da Transação: {produto['preco']}\n"
            f"⏳ Prazo para Pagamento: 15 Minutos\n\n"
            f"Por favor, faça o pagamento e clique no botão \"Já Paguei\" ou envie o comprovante para liberar o seu acesso!\n\n"
            f"💠 Chave Pix (e-mail): afjoaninha11@gmail.com\n"
        )
    )

    # Enviar chave PIX em formato mono
    await query.message.reply_text(
        f"💠 Copie a chave PIX abaixo para realizar o pagamento:\n\n`{produto['pix_chave']}`",
        parse_mode='MarkdownV2'
    )

    # Botões para copiar código e confirmar pagamento
    buttons = [
        [InlineKeyboardButton("🔄 Copiar Código PIX", callback_data=f"copiar_pix_{produto_key}")],
        [InlineKeyboardButton("✅ Já Paguei", callback_data="confirmar_pagamento")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text("Escolha uma das opções abaixo:", reply_markup=reply_markup)

async def copiar_pix(update: Update, context):
    query = update.callback_query
    produto_key = query.data.split('_')[-1]  # Extrair a parte correta da chave

    # Mensagem de depuração para verificar o valor extraído
    print(f"Produto Key extraído: {produto_key}")

    produto = produtos.get(produto_key)  # Usar get para evitar KeyError

    if produto is None:
        await query.answer("🚫 Código PIX não encontrado!", show_alert=True)
        return

    # Copiar código PIX para a área de transferência
    pyperclip.copy(produto["pix_chave"])
    
    await query.answer("📋 Código PIX copiado para a área de transferência!", show_alert=True)

async def confirmar_pagamento(update: Update, context):
    await update.callback_query.answer("📝 Por favor, envie o comprovante de pagamento para o suporte: t.me/liam_cris", show_alert=True)
    await update.callback_query.message.reply_text("💬 Contato de suporte: [@Liam_Cris](t.me/liam_cris)", parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token("7048165864:AAG_wsVMyueFg24qN12IQ2uE8udvVF3pdH4").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="^produto_"))
    app.add_handler(CallbackQueryHandler(copiar_pix, pattern="^copiar_pix_"))
    app.add_handler(CallbackQueryHandler(confirmar_pagamento, pattern="^confirmar_pagamento$"))
    
    app.run_polling()

if __name__ == "__main__":
    main()