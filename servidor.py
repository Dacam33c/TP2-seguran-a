import socket
import json
import time
import ssl
import hashlib

class Servidor:
    #inicializa o servidor em 'localgost', porta 4900 e maximo de 5 conexões simultaneas
    def __init__(self, endereco_servidor='localhost', porta_servidor=4900, max_conexoes=5):

        #cria um socket inicialmente sem nada de segurança
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #gera um contexto ssl a partir da biblioteca ssl
        #inclui o protocolo a ser utilizado, certificado de autenticação, 
        #chaves de criptografia e verificação de certificados.
        contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #pega o certificado e chave privada
        contexto_ssl.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        #faz a associação entre o socket criado e o ip e porta
        self.socket.bind((endereco_servidor, porta_servidor))
        #socket esta escutando, esperando conexões
        self.socket.listen(max_conexoes)
        
        #transforma o socket inicial em um socket seguro com ssl
        self.socket = contexto_ssl.wrap_socket(self.socket, server_side=True)
        
        print(f"Server ta em: {endereco_servidor}:{porta_servidor}")
        self.loopServidor()

    def loopServidor(self):
        while True:
            timeout = 300
            self.socket.settimeout(timeout)  
            try:
                #tenta aceitar a conexão para receber dados do cliente
                (socketParaCliente, enderecoDoCliente) = self.socket.accept()
                #recebe até 256 bytes
                pacote = socketParaCliente.recv(256)
            except TimeoutError as e:
                print(
                    f"{timeout} segundos se passaram e não houve tentiva de conexão")
                break
            except Exception as e: 
                print(e)
                break
            
            #transforma de bytes pra algo que possamos ler
            rqst = json.loads(pacote.decode("utf-8"))
            print(
                f"Servidor recebeu do cliente {enderecoDoCliente} a mensagem: {rqst}")
            
            respBytes = self.handler(rqst).encode("utf-8") 
            
            print(
                f"Servidor enviou para cliente cliente {enderecoDoCliente} a mensagem: {respBytes.decode('utf-8')}")


            #envia a resposta para o cliente. tenta 2 vezes por garantia
            socketParaCliente.send(respBytes)
            time.sleep(.1)
            socketParaCliente.send(respBytes) 

   



        #define como responder o cliente. no caso ele só manda a string "teste retorno" junto com o texto recebido na requisição 
        #tabém checa se o hash está correto
        #só pra testar se ta recebendo e enviando dados corretamente
    def handler(self, rqst):
        print(rqst)

        try:
            mensagem = rqst.get("request", "")
            hash_recebido = rqst.get("hash", "")

            # Recalcular o hash e comparar
            hash_calculado = calcular_hash(mensagem)

            if hash_calculado != hash_recebido:
                return json.dumps({"error": "Hash não corresponde! Mensagem pode ter sido alterada."})

            rtrn = "teste retorno"
        except TypeError as e:
            rtrn = f"Error: {str(e)}"

        resp = {
            "rqst": rqst,
            "retorno": rtrn
        }
        print(resp)
        return json.dumps(resp)

#aplica o sha256 para melhorar a segurança da mensagem
def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()

print('servidor')
server = Servidor()
print("SERVIDOR ENCERRADO")
del server 