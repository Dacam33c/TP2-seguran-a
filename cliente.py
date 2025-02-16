import socket
import time
import json
import ssl
import hashlib

def make_rqst(texto):
    #cria um contexto para o cliente, semelhante ao que fizemos no servidor
    contexto_ssl = ssl.create_default_context()
    #nós não fazemos uma verificação rigorosa no certificado pq somos nós mesmos que estamos assinando
    contexto_ssl.check_hostname = False
    contexto_ssl.verify_mode = ssl.CERT_NONE


    #conectando um socket para o cliente na mesma porta do servidor
    with socket.create_connection(('localhost', 4900)) as socketCliente:
        #transformamos o socket do cliente em um socket seguro
        with contexto_ssl.wrap_socket(socketCliente, server_hostname='localhost') as ssock:
            #aplica o sha256 sobre o texto
            hash_mensagem = calcular_hash(texto)
            rqst = {"request": texto, "hash": hash_mensagem}
            print(f"Enviando: {rqst}")

            #request é enviado em bytes
            rqstBytes = json.dumps(rqst).encode("utf-8")

            ssock.settimeout(3)
            tentativas = 0
            resp = None

            #fazemos um número de tentativas de envio dos dados, nesse caso 3 vezes
            while tentativas < 3:
                tentativas += 1
                try:
                    #envia os dados
                    ssock.send(rqstBytes)
                    #recebe a resposta
                    respBytes = ssock.recv(256).decode("utf-8")
                    #converte os bytes em um texto legível(json)
                    resp = json.loads(respBytes)
                    #casos de erro
                    if "retorno" in resp and resp["retorno"] is not None:
                        break
                except TimeoutError:
                    print("Tentativa de conexão falhou, tentando novamente...")
                #espera um pouco entra cada tentativa
                time.sleep(1)

            if resp is not None:
                return resp
            else:
                return False

#função para calcular o hash
def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()

#recebe uma string do teclado e manda para o servidor
def main():
    print("Cliente")

    entrada = input("Digite uma mensagem para o servidor: ")
    
    resposta = make_rqst(entrada)
    
    print(f"Resposta do servidor: {resposta}")

if __name__ == "__main__":
    main()
