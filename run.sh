#!/bin/bash

# Script para executar o Bot de Resumo dos Gerentes

echo "===================================="
echo "Bot de Resumo dos Gerentes"
echo "===================================="
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Criando arquivo .env a partir do template..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Edite-o com suas credenciais do Telegram."
    echo ""
    echo "Instruções:"
    echo "1. Abra o arquivo .env"
    echo "2. Adicione o BOT_TOKEN do seu bot (obtenha via @BotFather no Telegram)"
    echo "3. Salve o arquivo"
    echo "4. Execute este script novamente"
    exit 1
fi

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não foi encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python 3 encontrado"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "🤖 Iniciando o Bot..."
echo ""

# Executar o bot
python3 bot.py
