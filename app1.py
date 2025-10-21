from flask import Flask, request, jsonify

app = Flask(__name__)

DDDs_bloqueados = {'21', '85', '98'}  # DDDs bloqueados

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    numero = data["contacts"][0]["wa_id"]
    ddd = numero[2:4]

    # Se DDD bloqueado → ignora completamente
    if ddd in DDDs_bloqueados:
        print(f"Mensagem de {numero} ignorada (DDD bloqueado)")
        return jsonify({"status": "ignored"}), 200

    # Se permitido → aqui você processa a mensagem normalmente
    print(f"Mensagem de {numero} aceita")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
