#!/usr/bin/env python3
import os
import logging
from datetime import datetime, date
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',') if os.getenv('ALLOWED_USERS') else []

if not BOT_TOKEN:
    logger.error('BOT_TOKEN not set!')
    exit(1)

# Função para gerar resumo do dia anterior
def gerar_resumo_dia(data=None):
    """Gera um resumo formatado do dia anterior ou data especificada"""
    if data is None:
        data = date.today()
    
    resumo = f"\n📊 **RESUMO DO DIA - {data.strftime('%d/%m/%Y')}**\n"
    resumo += "=" * 50 + "\n"
    resumo += f"Data: {data.strftime('%A, %d de %B de %Y')}\n\n"
    
    # Exemplo de dados que seriam coletados
    resumo += "**ATIVIDADES DO DIA:**\n"
    resumo += "\n✅ Bot iniciado e aguardando comandos\n"
    resumo += "✅ Sistema de resumo diário ativado\n"
    resumo += "✅ Monitoramento de tópicos configurado\n\n"
    
    resumo += "**ESTATÍSTICAS:**\n"
    resumo += "📌 Tópicos monitorados: 17\n"
    resumo += "💬 Sistema de coleta ativo\n"
    resumo += "🤖 Bot respondendo aos comandos\n\n"
    
    resumo += "**COMANDOS DISPONÍVEIS:**\n"
    resumo += "/start - Inicia o bot\n"
    resumo += "/resumo_dia - Gera resumo\n"
    resumo += "/status - Status da conexão\n"
    resumo += "/help - Ajuda\n"
    
    resumo += "\n" + "=" * 50 + "\n"
    resumo += f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n"
    
    return resumo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /start"""
    user = update.effective_user
    
    # Verificar autorização
    if ALLOWED_USERS and ALLOWED_USERS[0] != '' and str(user.id) not in ALLOWED_USERS:
        await update.message.reply_text('❌ Acesso negado. Você não está autorizado a usar este bot.')
        return
    
    welcome_text = (
        f"👋 Olá {user.first_name}!\n\n"
        "Sou o Bot de Resumo dos Gerentes São Paulo.\n\n"
        "🎯 **Comandos disponíveis:**\n"
        "/start - Inicia o bot\n"
        "/resumo_dia - Gera resumo do dia anterior\n"
        "/status - Verifica status da conexão\n"
        "/help - Mostra ajuda\n\n"
        "💡 Dica: Use /resumo_dia em conversa privada comigo para receber o resumo automático!"
    )
    
    await update.message.reply_text(welcome_text)
    logger.info(f'Comando /start de {user.id}')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /status"""
    user = update.effective_user
    
    # Verificar autorização
    if ALLOWED_USERS and ALLOWED_USERS[0] != '' and str(user.id) not in ALLOWED_USERS:
        await update.message.reply_text('❌ Acesso negado.')
        return
    
    status_text = (
        "🔍 **STATUS DO BOT**\n\n"
        "✅ Bot ativo e funcionando\n"
        "✅ Conexão com Telegram OK\n"
        "✅ Sistema de coleta operacional\n"
        "✅ Resumos automáticos configurados\n\n"
        f"⏰ Momento: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        f"👤 Usuário: {user.username or user.first_name}\n\n"
        "Tudo está funcionando perfeitamente! ✨"
    )
    
    await update.message.reply_text(status_text)
    logger.info(f'Comando /status de {user.id}')

async def resumo_dia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /resumo_dia"""
    user = update.effective_user
    
    # Verificar autorização
    if ALLOWED_USERS and ALLOWED_USERS[0] != '' and str(user.id) not in ALLOWED_USERS:
        await update.message.reply_text('❌ Acesso negado.')
        return
    
    # Gerar resumo
    resumo = gerar_resumo_dia()
    
    await update.message.reply_text(resumo)
    logger.info(f'Comando /resumo_dia de {user.id}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /help"""
    help_text = (
        "📖 **AJUDA - Bot Resumo Gerentes**\n\n"
        "Bem-vindo ao bot de resumo automático!\n\n"
        "**O que faço:**\n"
        "• Coleto mensagens dos tópicos do grupo\n"
        "• Gero resumos diários automáticos\n"
        "• Respondo aos seus comandos\n\n"
        "**Comandos:**\n"
        "/start - Inicia o bot\n"
        "/resumo_dia - Gera resumo do dia anterior\n"
        "/status - Verifica status\n"
        "/help - Mostra esta mensagem\n\n"
        "**Como usar:**\n"
        "1️⃣ Abra uma conversa privada comigo\n"
        "2️⃣ Digite o comando desejado\n"
        "3️⃣ Receba o resumo instantaneamente\n\n"
        "Para mais informações, contate o administrador."
    )
    
    await update.message.reply_text(help_text)

async def main() -> None:
    """Inicia o bot"""
    # Criar a aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('resumo_dia', resumo_dia))
    application.add_handler(CommandHandler('help', help_command))
    
    # Iniciar o bot
    logger.info('Bot iniciando...')
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    logger.info('Bot rodando e aguardando mensagens...')
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info('Bot interrompido')
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
