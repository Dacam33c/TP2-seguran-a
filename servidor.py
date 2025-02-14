import socket
import json
import time


class Servidor:
    def __init__(self, endereco_servidor='localhost', porta_servidor=4900, max_conexoes=5):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((endereco_servidor, porta_servidor))
        self.socket.listen(max_conexoes)
        self.loopServidor()

    def loopServidor(self):
        while True:
            timeout = 300
            self.socket.settimeout(timeout)  
            try:
                (socketParaCliente, enderecoDoCliente) = self.socket.accept()
                pacote = socketParaCliente.recv(256)
            except TimeoutError as e:
                print(
                    f"{timeout} segundos se passaram e não houve tentiva de conexão")
                break
            except Exception as e: 
                print(e)
                break

            rqst = json.loads(pacote.decode("utf-8"))
            print(
                f"Servidor recebeu do cliente {enderecoDoCliente} a mensagem: {rqst}")
            
            respBytes = self.handler(rqst).encode("utf-8") 
            
            print(
                f"Servidor enviou para cliente cliente {enderecoDoCliente} a mensagem: {respBytes.decode('utf-8')}")



            socketParaCliente.send(respBytes)
            time.sleep(.1)
            socketParaCliente.send(respBytes) 

    def handler(self, rqst):
        print(rqst)

        try:
            rtrn = "teste retorno"
        except TypeError as e:
            rtrn = f"Error: {str(e)}"

        resp = {
               "rqst": rqst,
               
                "retorno": rtrn
               }
        print(resp)
        return json.dumps(resp) 


server = Servidor()
print("SERVIDOR ENCERRADO")
del server 