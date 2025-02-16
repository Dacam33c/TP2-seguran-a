from flask import Flask, request, jsonify
import hashlib
import ssl

app = Flask(__name__)

def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()

@app.route('/mensagem', methods=['POST'])
def receber_mensagem():
    try:
        dados = request.json  # Obtém os dados JSON da requisição
        mensagem = dados.get("request", "")
        hash_recebido = dados.get("hash", "")

        # Recalcula o hash para verificar a integridade
        hash_calculado = calcular_hash(mensagem)

        if hash_calculado != hash_recebido:
            return jsonify({"error": "Hash errado n pode n"}), 400

        return jsonify({"retorno": "Deu certo :D"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')  # Certificados SSL
    app.run(host='0.0.0.0', port=4900, ssl_context=context, debug=True)
