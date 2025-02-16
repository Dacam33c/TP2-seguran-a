import requests
import hashlib
import json

#função para calcular hash sha256
def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()

#faz requisição https com o texto
def make_rqst(texto):
    #define o ulr a ser usado
    url = "https://localhost:4900/mensagem"

    # Calcula o hash da mensagem
    hash_mensagem = calcular_hash(texto)

    # Envia a requisição https com json
    payload = {"request": texto, "hash": hash_mensagem}
    headers = {"Content-Type": "application/json"}

    #tenta fazer o envio com metodo post
    try:
        #o certificado é assinado por nos mesmos entao a verificação fica como falsa
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return response.json()
    #casos de erro:
    except requests.exceptions.SSLError:
        print("Erro SSL :( Verifica o servidor")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


# roda o cliente 
if __name__ == "__main__":
    entrada = input("Digita alguma coisa: ")
    resposta = make_rqst(entrada)
    print(f"Resposta do servidor: {resposta}")
