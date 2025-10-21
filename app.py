from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ⚙️ Configurações
ACCESS_TOKEN = "EAAQBO3qp4LoBPjW74qQWb9FQeS5K6coZC571xkPMImM04vaj4hos5opxs9BgyYgWAwn8OLySQRosfLDXqQK7CoQ4IZAxMVYVWgA7VGZC8QxMaKKwIwSbvaLz8hwKvVdRmmqfBNSfqHlAcMKR6A64FhSdNn2QO7aBhfXmzOBCz1kQe4HkZABHMKD2t0OlAxxHW2hBwaJ7T2gcvsZCmWZClBfeHtLbHDU3BJCJhZBc91xI9gAQy3A0JAkUCXZComsZD"
PHONE_NUMBER_ID = "852467524612557"
API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# Bloquear DDDs
DDDs_bloqueados = {'51', '42'}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    numero = data["contacts"][0]["wa_id"]
    ddd = numero[2:4]

    # 🔒 Bloqueia mensagens desses DDDs
    if ddd in DDDs_bloqueados:
        print(f"Mensagem de {numero} bloqueada (DDD {ddd})")
        return jsonify({"status": "blocked"}), 200

    # ✅ Caso contrário, responde normalmente
    mensagem = "Olá! Sua mensagem foi recebida com sucesso."
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": mensagem}
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}",
               "Content-Type": "application/json"}
    requests.post(API_URL, json=payload, headers=headers)

    print(f"Mensagem de {numero} aceita e respondida.")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
