#!/usr/bin/env python3
import os
import logging
from datetime import datetime, time, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from collections import defaultdict
import asyncio

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
SENIOR_URL = os.getenv('SENIOR_URL', 'https://seu-servidor-senior.com')
SENIOR_USER = os.getenv('SENIOR_USER', 'seu_usuario')
SENIOR_PASSWORD = os.getenv('SENIOR_PASSWORD', 'sua_senha')
ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',')

# Store data
managers_data = {}
last_summary_time = None

if not BOT_TOKEN:
    logger.error('BOT_TOKEN not set!')
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = update.effective_user
    if str(user.id) not in ALLOWED_USERS and ALLOWED_USERS[0] != '':
        await update.message.reply_text('Acesso negado.')
        return
    
    welcome_text = (
        'Olá! Sou o bot de resumo de gerentes.\n\n'
        'Comandos disponíveis:\n'
        '/start - Inicia o bot\n'
        '/status - Mostra status de conexão com Senior\n'
        '/resumo_dia - Gera resumo do dia\n'
        '/help - Mostra ajuda'
    )
    await update.message.reply_text(welcome_text)
    logger.info(f'Start command from user {user.id}')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check connection status with Senior"""
    user = update.effective_user
    if str(user.id) not in ALLOWED_USERS and ALLOWED_USERS[0] != '':
        await update.message.reply_text('Acesso negado.')
        return
    
    status_text = '🔍 Verificando status da integração Senior...\n'
    
    try:
        # Try to connect to Senior API
        response = requests.get(
            f'{SENIOR_URL}/api/status',
            auth=(SENIOR_USER, SENIOR_PASSWORD),
            timeout=5
        )
        
        if response.status_code == 200:
            status_text += '✅ Conectado com sucesso!\n'
            status_text += f'Servidador Senior: {SENIOR_URL}\n'
            status_text += f'Usuários autorizados: {len(ALLOWED_USERS)}\n'
        else:
            status_text += f'⚠️ Erro: Status {response.status_code}\n'
    except requests.exceptions.ConnectionError:
        status_text += '❌ Não consegui conectar ao Senior\n'
    except Exception as e:
        status_text += f'❌ Erro: {str(e)}\n'
    
    await update.message.reply_text(status_text)
    logger.info(f'Status command from user {user.id}')

async def resumo_dia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate daily summary"""
    user = update.effective_user
    if str(user.id) not in ALLOWED_USERS and ALLOWED_USERS[0] != '':
        await update.message.reply_text('Acesso negado.')
        return
    
    summary_text = '📊 **Resumo do Dia - Gerentes**\n'
    summary_text += '=' * 40 + '\n'
    summary_text += f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n\n'
    
    try:
        # Fetch data from Senior
        response = requests.get(
            f'{SENIOR_URL}/api/gerentes',
            auth=(SENIOR_USER, SENIOR_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list):
                summary_text += f'Total de Gerentes: {len(data)}\n\n'
                
                for gerente in data[:10]:  # Show first 10
                    summary_text += f'👤 {gerente.get("nome", "N/A")}\n'
                    summary_text += f'   Status: {gerente.get("status", "N/A")}\n'
                    summary_text += f'   Última atualização: {gerente.get("ultima_atualizacao", "N/A")}\n\n'
                
                if len(data) > 10:
                    summary_text += f'... e mais {len(data) - 10} gerentes\n'
            else:
                summary_text += 'Dados recebidos com sucesso!\n'
        else:
            summary_text += f'⚠️ Erro ao buscar dados: {response.status_code}\n'
    except Exception as e:
        summary_text += f'❌ Erro: {str(e)}\n'
    
    summary_text += '\n' + '=' * 40 + '\n'
    await update.message.reply_text(summary_text)
    logger.info(f'Resumo command from user {user.id}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = (
        '📖 **AJUDA - Bot Resumo Gerentes**\n\n'
        'Este bot integra com seu sistema Senior para gerar resumos.\n\n'
        '**Comandos:**\n'
        '/start - Inicia o bot\n'
        '/status - Verifica conexão com Senior\n'
        '/resumo_dia - Gera resumo diário\n'
        '/help - Mostra esta mensagem\n\n'
        '**Configuração:**\n'
        'Certifique-se de que as variáveis de ambiente estão configuradas:\n'
        '- BOT_TOKEN\n'
        '- SENIOR_URL\n'
        '- SENIOR_USER\n'
        '- SENIOR_PASSWORD\n'
        '- ALLOWED_USERS\n'
    )
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages"""
    logger.info(f'Message from {update.effective_user.id}: {update.message.text[:50]}')

async def main() -> None:
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    application.add_handler(CommandHandler('resumo_dia', resumo_dia))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    logger.info('Bot started and polling')
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info('Bot stopped')
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
