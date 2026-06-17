import os
import time
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

#Supabase 
SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

#Z-API 
ZAPI_INSTANCE_ID: str = os.environ["ZAPI_INSTANCE_ID"]
ZAPI_TOKEN: str       = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN: str = os.environ["ZAPI_CLIENT_TOKEN"]   # header Security-Token
ZAPI_BASE_URL: str    = (
    f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}"
)

MAX_CONTACTS = 3          
DELAY_SECONDS = 2      


def get_contacts(supabase: Client) -> list[dict]:
    """Busca até MAX_CONTACTS contatos ativos no Supabase."""
    response = (
        supabase.table("contacts")
        .select("name, phone")
        .eq("active", True)
        .limit(MAX_CONTACTS)
        .execute()
    )
    return response.data or []


def send_whatsapp(phone: str, name: str) -> dict:
    """
    Envia mensagem via Z-API para o número informado.
    O telefone deve estar no formato E.164 sem '+': ex. 5511999999999
    """
    message = f"Olá, {name} tudo bem com você?"
    url = f"{ZAPI_BASE_URL}/send-text"

    payload = {
        "phone": phone,
        "message": message,
    }
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def main() -> None:
    print("🔌 Conectando ao Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    contacts = get_contacts(supabase)

    if not contacts:
        print("⚠️  Nenhum contato encontrado na tabela 'contacts'.")
        return

    print(f"📋 {len(contacts)} contato(s) encontrado(s). Iniciando envios...\n")

    success, errors = 0, 0

    for contact in contacts:
        name  = contact.get("name", "").strip()
        phone = contact.get("phone", "").strip()

        if not name or not phone:
            print(f"  ⚠️  Contato inválido (sem nome ou telefone): {contact}")
            errors += 1
            continue

        try:
            result = send_whatsapp(phone, name)
            print(f"  ✅ Mensagem enviada para {name} ({phone}): {result}")
            success += 1
        except requests.HTTPError as exc:
            print(f"  ❌ Erro HTTP ao enviar para {name} ({phone}): {exc.response.text}")
            errors += 1
        except Exception as exc:
            print(f"  ❌ Erro ao enviar para {name} ({phone}): {exc}")
            errors += 1

        if contact != contacts[-1]:          
            time.sleep(DELAY_SECONDS)

    print(f"\n📊 Resultado: {success} enviado(s) | {errors} erro(s)")


if __name__ == "__main__":
    main()
