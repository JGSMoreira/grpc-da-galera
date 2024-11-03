import chat_pb2
import chat_pb2_grpc
import json
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

with open('config.json', 'r') as f:
            global config 
            config = json.load(f)

def usuarios(self):
    users = ', '.join([user['name'] for user in self.users])
    self.notify_clients(f"Usuários conectados: {users}")
    return chat_pb2.Empty()

def motd(self):
    self.notify_clients(f"{config['motd']}")
    return chat_pb2.Empty()

def ping(self):
    self.notify_clients("Pong!")
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
        whisper = chat_pb2.ChatMessage(name="Servidor", text=f"{request.name} sussurrou você: {mensagem}", timestamp=timestamp)

        self.clients[destinatario].append(whisper)
        print(f"{request.name} sussurrou para {destinatario}: {mensagem}")
    else:
        print(f"{request.name} tentou sussurrar para {destinatario}, mas o usuário não foi encontrado.")
    
    return chat_pb2.Empty()

