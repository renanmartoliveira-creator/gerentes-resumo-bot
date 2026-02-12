# SETUP GUIDE - Gerentes Resumo Bot

## Informações do Bot Criado

**Bot Username**: @gerentes_resumo_bot
**Bot Token**: `8466686351:AAENIzXmszt9enUHhnfaUtWYM21Hv1hKnE`
**Data de Criação**: 12 de Fevereiro de 2026

## Próximos Passos

### 1. Obter IDs dos Grupos

Para fazer o bot funcionar, você precisa dos IDs numéricos dos dois grupos:

**Grupo Origem**: "Gerentes São Paulo"
**Grupo Resumo**: "Resumo Gerentes São Paulo"

Para obter os IDs:
1. Abra o Telegram Web em https://web.telegram.org
2. Abra o grupo desejado
3. Copie o número que aparecer na URL (ex: `https://web.telegram.org/k/#-2360921767`)
4. Adicione um prefixo `-100` ao número (ex: `-1002360921767`)

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com:

```
API_ID=your_api_id_from_my.telegram.org
API_HASH=your_api_hash_from_my.telegram.org
BOT_TOKEN=8466686351:AAENIzXmszt9enUHhnfaUtWYM21Hv1hKnE
GROUP_SOURCE_ID=-1001234567890  # ID do "Gerentes São Paulo"
GROUP_RESUME_ID=-1009876543210   # ID do "Resumo Gerentes São Paulo"
PERPLEXITY_API_KEY=pk_your_key    # Opcional
```

### 3. Obter API_ID e API_HASH

1. Acesse https://my.telegram.org
2. Faça login com sua conta Telegram
3. Clique em "API development tools"
4. Crie uma nova app (se não tiver)
5. Copie o App ID e App Hash

### 4. Deploy no Render

1. Acesse https://render.com
2. Crie uma conta e faça login
3. Crie um novo "Web Service"
4. Conecte com este repositório GitHub
5. Configure as variáveis de ambiente no painel
6. Deploy será feito automaticamente

### 5. Adicionar Bot aos Grupos

1. Abra o bot: https://t.me/gerentes_resumo_bot
2. Clique em "Start" ou abra a conversa
3. Volte ao grupo "Gerentes São Paulo"
4. Adicione o bot como membro
5. Promova o bot a admin (necessário para ler mensagens dos tópicos)
6. Repita para o grupo "Resumo Gerentes São Paulo"

## Comandos Disponíveis

- `/resumo_dia` - Gera resumo do dia atual
- `/relatorio_pessoa @username` - Relatório personalizado (em desenvolvimento)
- `/contagem_msgs` - Estatísticas de mensagens (em desenvolvimento)

## Testes

Antes de colocar em produção:

1. Execute localmente: `python bot.py`
2. Envie uma mensagem em um dos tópicos monitorados
3. Verifique se o bot recebe a mensagem nos logs
4. Teste o comando `/resumo_dia`
5. Verifique se os resumos são postados corretamente

## Troubleshooting

**Problema**: Bot não está coletando mensagens
**Solução**: Verifique se o bot é admin no grupo

**Problema**: Erro de autenticação
**Solução**: Verifique se o BOT_TOKEN está correto no arquivo `.env`

**Problema**: Resumos não são postados
**Solução**: Verifique se os IDs dos grupos estão corretos

## Suporte

Para dúvidas ou problemas, abra uma issue neste repositório.
