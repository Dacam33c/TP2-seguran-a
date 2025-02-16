from flask import Flask, request, jsonify, render_template_string
import ssl

app = Flask(__name__)

# ultima mensagem recebida
ultima_mensagem = "N mandaram nada ainda n. envia uma mensagem pelo cliente e recarrega a pagina"


@app.route('/mensagem', methods=['POST', 'GET'])
def receber_mensagem():
    global ultima_mensagem  # pra modificar a mensagem q vai aparecer na tela

    #se usarmos o metodo post
    if request.method == 'POST':
        #tenta ler os dados da forma json
        try:
            dados = request.json
            #pega a mensagem na chave "request"
            mensagem = dados.get("request", "")
            #atualiza mensagem
            ultima_mensagem = mensagem
            
            return jsonify({"retorno": f"Mensagem: {mensagem}"})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    # html para mostrar a mensagem
    html = f"""
    <html>
        <head>
            <title>Última Mensagem</title>
        </head>
        <body>
            <h1>Última Mensagem Recebida:</h1>
            <p>{ultima_mensagem}</p>
        </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    # certificado e chave privada que estão salvos na pasta do projeto
    cert_path = "cert.pem"
    key_path = "key.pem"

    #inicia o servidor Flask com https, com um contexto ssl
    #ou seja inclui certificado, validação e chaves de criptografia
    app.run(host="0.0.0.0", port=4900, ssl_context=(cert_path, key_path))
