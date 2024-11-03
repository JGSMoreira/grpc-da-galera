import chat_pb2
import chat_pb2_grpc
import json
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

with open('config.json', 'r') as f:
            global config 
            config = json.load(f)

def usuarios(self, request):
    users = ', '.join([user['name'] for user in self.users])
    mensagem_usuario_especifico(self, request.name, f"Usuários conectados: {users}")
    return chat_pb2.Empty()

def motd(self, request):
    mensagem_usuario_especifico(self, request.name, f"{config['motd']}")
    return chat_pb2.Empty()

def ping(self, request):
    mensagem_usuario_especifico(self, request.name, "Pong!")
    return chat_pb2.Empty()
    
def sussurrar(self, request, context):
    comando = request.text.split(' ', 2)
    if len(comando) < 3:
        return chat_pb2.Empty()

    destinatario = comando[1]
    mensagem = comando[2]

    if destinatario in self.clients:
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now())
        whisper = chat_pb2.ChatMessage(name="Servidor", text=f"{request.name} sussurrou '{mensagem}' você.", timestamp=timestamp)

        self.clients[destinatario].append(whisper)
        print(f"{request.name} sussurrou para {destinatario}: {mensagem}")
    else:
        print(f"{request.name} tentou sussurrar para {destinatario}, mas o usuário não foi encontrado.")
    
    return chat_pb2.Empty()

def ajuda(self, request):
    mensagem_usuario_especifico(self, request.name, "Comandos disponíveis: /usuarios, /motd, /ping, /sussurrar <usuário> <mensagem>")
    return chat_pb2.Empty()

def mensagem_usuario_especifico(self, destinatario, mensagem):
    if destinatario in self.clients:
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now())
        print(f"Servidor: {mensagem}")
        whisper = chat_pb2.ChatMessage(name="Servidor", text=f"{mensagem}", timestamp=timestamp)

        self.clients[destinatario].append(whisper)