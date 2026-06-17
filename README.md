# 📲 WhatsApp Bot — Supabase + Z-API

Lê contatos cadastrados no **Supabase** e envia mensagens personalizadas via **Z-API** (WhatsApp).

```
Olá, <nome_contato> tudo bem com você?
```

---

## 🗂️ Estrutura

```
whatsapp-supabase/
├── src/
│   └── main.py              # script principal
├── docs/
│   └── supabase_setup.sql   # SQL para criar a tabela de contatos
├── .env.example             # variáveis de ambiente (modelo)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Passo a passo

### 1 · Supabase — criar a tabela

1. Acesse [supabase.com](https://supabase.com) e crie um projeto gratuito.
2. Vá em **SQL Editor → New Query**, cole o conteúdo de [`docs/supabase_setup.sql`](docs/supabase_setup.sql) e clique em **Run**.
3. Edite os registros inseridos com nomes e telefones reais (formato `5511999999999`).
4. Copie a **URL** e a **anon key** em *Project Settings → API*.

### 2 · Z-API — obter credenciais

1. Crie uma conta gratuita em [z-api.io](https://www.z-api.io).
2. Crie uma instância e conecte seu WhatsApp via QR Code.
3. No painel da instância anote:
   - **Instance ID**
   - **Token**
   - **Security Token** (Client-Token)

### 3 · Configurar variáveis de ambiente

```bash
cp .env.example .env
```

### 4 · Instalar dependências e executar

```bash
python -m venv .venv
source .venv/bin/activate      # ! Windows: .venv\Scripts\activate

pip install -r requirements.txt

python src/main.py
```

**Saída esperada:**

```
🔌 Conectando ao Supabase...
📋 3 contato(s) encontrado(s). Iniciando envios...

  ✅ Mensagem enviada para Maria Silva (5511991234567): {'zaapId': '...', 'messageId': '...'}
  ✅ Mensagem enviada para João Pereira (5521987654321): {'zaapId': '...', 'messageId': '...'}
  ✅ Mensagem enviada para Ana Souza (5531912345678): {'zaapId': '...', 'messageId': '...'}

📊 Resultado: 3 enviado(s) | 0 erro(s)
```

---

## ⚙️ Variáveis de ambiente

| Variável | Onde encontrar |
|---|---|
| `SUPABASE_URL` | Project Settings → API → Project URL |
| `SUPABASE_KEY` | Project Settings → API → anon/public key |
| `ZAPI_INSTANCE_ID` | Painel Z-API → sua instância |
| `ZAPI_TOKEN` | Painel Z-API → sua instância |
| `ZAPI_CLIENT_TOKEN` | Painel Z-API → Security Token |

---

## 📌 Regras de negócio

| Regra | Implementação |
|---|---|
| Máximo 3 contatos | constante `MAX_CONTACTS = 3` em `main.py` |
| Personalizar nome | `"Olá, {name} tudo bem com você?"` |
| Apenas contatos ativos | `.eq("active", True)` na query Supabase |
| Pausa entre envios | `DELAY_SECONDS = 2` para evitar bloqueio |

---

## 🛠️ Tecnologias

- **Python 3.11+**
- [supabase-py](https://github.com/supabase-community/supabase-py) — cliente oficial do Supabase
- [requests](https://docs.python-requests.org) — chamadas HTTP para a Z-API
- [python-dotenv](https://github.com/theskumar/python-dotenv) — leitura do `.env`
