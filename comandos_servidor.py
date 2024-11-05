import chat_pb2
import grpc
import json
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import requests

with open('config.json', 'r') as f:
            global config 
            config = json.load(f)
            
def mensagem_usuario_especifico(self, destinatario, mensagem):
    if destinatario in self.clients:
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.now())
        print(f"Servidor: {mensagem}")
        whisper = chat_pb2.ChatMessage(name="Servidor", text=f"{mensagem}", timestamp=timestamp)

        self.clients[destinatario].append(whisper)
        
# Comandos abertos a todos os usuários

# /ajuda
def ajuda(self, request):
    mensagem = """
    Comandos disponíveis:
    /usuarios - Lista os usuários conectados
    /motd - Exibe a mensagem do dia
    /ping - Testa a conexão com o servidor
    /sussurrar <usuário> <mensagem> - Envia uma mensagem privada para um usuário
    /fm - Exibe uma frase motivacional
    
    Comandos de administrador:
    /expulsar <usuário> - Expulsa um usuário do chat
    /banir <usuário> - Bane um usuário do chat
    """
    mensagem_usuario_especifico(self, request.name, mensagem)
    return chat_pb2.Empty()


# /usuarios
def usuarios(self, request):
    users = ', '.join([user['name'] for user in self.users])
    mensagem_usuario_especifico(self, request.name, f"Usuários conectados: {users}")
    return chat_pb2.Empty()

# /motd
def motd(self, request):
    mensagem_usuario_especifico(self, request.name, f"{config['motd']}")
    return chat_pb2.Empty()

# /ping
def ping(self, request):
    mensagem_usuario_especifico(self, request.name, "Pong!")
    return chat_pb2.Empty()

# /sussurrar <usuário> <mensagem> 
def sussurrar(self, request):
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

# /fm
def frase_motivacional(self, request):
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()

    if data:
        frase = data[0]['q']
        autor = data[0]['a']
        mensagem = f"Frase motivacional: '{frase}' - {autor}"
    else:
        mensagem = "Não foi possível obter a frase motivacional."

    mensagem_usuario_especifico(self, request.name, mensagem)
    return chat_pb2.Empty()


# Comandos disponíveis apenas para administradores

# /expulsar <usuário>
def expulsar(self, request):
    comando = request.text.split(' ', 2)
    if len(comando) < 2:
        return chat_pb2.Empty()
    
    if request.name not in config['admins']:
        mensagem_usuario_especifico(self, request.name, "Você não tem permissão para executar este comando")
        return chat_pb2.Empty()

    destinatario = comando[1]

    if destinatario in self.clients:
        self.pool_remocao.append(destinatario)

        print(f"{request.name} expulsou {destinatario} do chat.")
    else:
        print(f"{request.name} tentou expulsar {destinatario}, mas o usuário não foi encontrado.")
    
    return chat_pb2.Empty()

# /banir <usuário>
def banir(self, request):
    comando = request.text.split(' ', 2)
    if len(comando) < 2:
        return chat_pb2.Empty()
    
    if request.name not in config['admins']:
        mensagem_usuario_especifico(self, request.name, "Você não tem permissão para executar este comando.")
        return chat_pb2.Empty()

    destinatario = comando[1]

    if destinatario in self.clients:
        config['black_list'].append(destinatario)
        self.banido_instancia.append(destinatario)
        self.pool_remocao.append(destinatario)
        
        print(f"{request.name} baniu {destinatario} do chat.")
    else:
        print(f"{request.name} tentou banir {destinatario}, mas o usuário não foi encontrado.")
    
    return chat_pb2.Empty()

    
