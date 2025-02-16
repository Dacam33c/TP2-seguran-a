import requests
import hashlib
import json

def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()

def make_rqst(texto):
    url = "https://localhost:4900/mensagem"

    # Calcula o hash da mensagem
    hash_mensagem = calcular_hash(texto)

    # Envia a requisição HTTPS com JSON
    payload = {"request": texto, "hash": hash_mensagem}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        return response.json()
    except requests.exceptions.SSLError:
        print("Erro SSL :( Verifica o servidor")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Teste do cliente
if __name__ == "__main__":
    entrada = input("Digita alguma coisa: ")
    resposta = make_rqst(entrada)
    print(f"Resposta do servidor: {resposta}")
