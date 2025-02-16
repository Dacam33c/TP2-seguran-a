import socket
import time
import json
import ssl

def make_rqst(texto):
    contexto_ssl = ssl.create_default_context()
    contexto_ssl.check_hostname = False  # Permite certificados autossinados
    contexto_ssl.verify_mode = ssl.CERT_NONE  # Desativa a verificação SSL (não recomendado para produção)

    with socket.create_connection(('localhost', 4900)) as socketCliente:
        with contexto_ssl.wrap_socket(socketCliente, server_hostname='localhost') as ssock:
            rqst = {"request": texto}  # Ajuste para JSON válido
            print(f"Enviando: {rqst}")

            rqstBytes = json.dumps(rqst).encode("utf-8")

            ssock.settimeout(3)
            tentativas = 0
            resp = None

            while tentativas < 3:
                tentativas += 1
                try:
                    ssock.send(rqstBytes)
                    respBytes = ssock.recv(256).decode("utf-8")
                    resp = json.loads(respBytes)
                    if "retorno" in resp and resp["retorno"] is not None:
                        break
                except TimeoutError:
                    print("Tentativa de conexão falhou, tentando novamente...")
                time.sleep(1)

            if resp is not None:
                return resp
            else:
                return False

def main():
    print("Cliente")

    entrada = input("Digite uma mensagem para o servidor: ")
    
    resposta = make_rqst(entrada)
    
    print(f"Resposta do servidor: {resposta}")

if __name__ == "__main__":
    main()
