import socket
import time
import json

def make_rqst():
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('localhost', 4900))

    rqst = "teste rqst"
    print(rqst)

    rqstBytes = json.dumps(rqst).encode("utf-8")

    socketCliente.settimeout(3)
    tentativas = 0
    resp = None

    while (tentativas < 3):
        tentativas += 1
        try:
            socketCliente.send(rqstBytes) 
            respBytes = socketCliente.recv(256).decode("utf-8")
            resp = json.loads(respBytes)
            if("retorno" in resp and resp["retorno"] is not None):
                break
        except TimeoutError:
            pass
        time.sleep(1)

        socketCliente.close()
    if (resp is not None):
        return resp["retorno"]
    else:
        return False


def main():
    print(make_rqst())

if __name__ == "__main__":
    main()
