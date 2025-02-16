Segurança coputacional Noturno TP-2 
João Pedro Carvalho - 221017032
Gabriel Maurício - 221017097

Para a realização do projeto foram utilizadas as bibliotecas flask, requests, haslib e ssl.
Modo de uso:
primeiro o servidor dever ser executado com python servidor.py
depois do servidor executamos o cliente com python cliente.py

o cliente então nos permite das uma entrada de texto que é enviada ao servidor e recebemos uma resposta
podemos visualizar a mensagem enviada acessando https://localhost:4900/mensagem
possivelmente a pagina sera marcada como não segura pois não estamos verificando a assinatura adequadamente, já que ela é autoassinada

Caso haja problemas com a chave/certificação o comando "openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes" é usado para gerar novos arquivos
