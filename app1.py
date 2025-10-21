from flask import Flask, request, jsonify

app = Flask(__name__)

# DDDs bloqueados
DDDs_bloqueados = {'51', '42'}

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificação do WhatsApp Cloud API
        token = "CPS1844LFCA"  # Defina qualquer token que você queira
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == token:
            return challenge, 200
        return "Token inválido", 403

    if request.method == "POST":
        data = request.json
        try:
            numero = data["contacts"][0]["wa_id"]
            ddd = numero[2:4]

            if ddd in DDDs_bloqueados:
                print(f"Mensagem de {numero} ignorada (DDD bloqueado)")
                return jsonify({"status": "ignored"}), 200

            print(f"Mensagem de {numero} aceita")
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

