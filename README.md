# Gerentes Resumo Bot

Bot Telegram para coleta, análise e resumo automatizado de mensagens dos tópicos do grupo Gerentes São Paulo.

## Funcionalidades

- ✅ **Coleta Automática de Mensagens**: Monitora todos os tópicos do grupo
- ✅ **Resumos Diários Agendados**: Gera resumos automaticamente às 23:59 de cada dia
- ✅ **Resumos por Tópico**: Organiza os resumos por tópico no grupo "Resumo Gerentes São Paulo"
- ✅ **Comando de Resumo Sob Demanda**: `/resumo_dia` para gerar resumo imediatamente
- ✅ **Integração com IA**: Utiliza Perplexity API para gerar resumos inteligentes

## Tópicos Monitorados

1. Tarefas
2. TODOS - Avisos
3. Chat geral
4. TODOS - Equipe
5. General
6. Links (planilhas e acessos)
7. Atualização
8. Hora extra
9. Analítica - Dados
10. TODOS - Ativar ST SERVICE
11. Eventos
12. Aprovados
13. TODOS - Deletar ST SERVICE
14. EPIs - Nome / Documento
15. Zona 2 - Preto
16. Zona 4 - Azul
17. Zona 1 - Vermelho

## Instalação

### Pré-requisitos

- Python 3.8+
- Conta Telegram
- Telegram Bot Token (obter via @BotFather)
- API ID e API Hash (obter em https://my.telegram.org)

### Setup Local

```bash
# Clonar repositório
git clone https://github.com/renanmartoliveira-creator/gerentes-resumo-bot.git
cd gerentes-resumo-bot

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Executar bot
python bot.py
```

## Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_telegram_bot_token
GROUP_SOURCE_ID=-1001234567890  # ID do grupo "Gerentes São Paulo"
GROUP_RESUME_ID=-1009876543210  # ID do grupo "Resumo Gerentes São Paulo"
PERPLEXITY_API_KEY=pk_your_key  # Opcional
```

## Deploy em Render

1. Fork este repositório
2. Crie uma conta em [Render.com](https://render.com)
3. Crie um novo Web Service
4. Selecione o repositório
5. Configure as variáveis de ambiente no painel do Render
6. Deploy automático será realizado

## Comandos do Bot

- `/resumo_dia` - Gera resumo do dia atual
- `/relatorio_pessoa` - Gera relatório personalizado (em desenvolvimento)
- `/contagem_msgs` - Mostra estatísticas de mensagens (em desenvolvimento)

## Estrutura do Projeto

```
.
├── bot.py                # Código principal do bot
├── requirements.txt       # Dependências Python
├── Procfile              # Configuração para deploy
├── .env.example          # Template de variáveis de ambiente
└── README.md             # Este arquivo
```

## Tecnologias Utilizadas

- **Telethon**: Biblioteca Python para Telegram Client API
- **Python 3.8+**: Linguagem de programação
- **Perplexity API**: IA para geração de resumos (opcional)
- **Render**: Plataforma de deploy em nuvem

## Licença

MIT License

## Suporte

Para reportar bugs ou sugerir features, abra uma issue no repositório.
