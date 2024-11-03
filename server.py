import grpc
import chat_pb2
import chat_pb2_grpc
from concurrent.futures import ThreadPoolExecutor
from grpc_reflection.v1alpha import reflection
from collections import deque
import signal
import sys
import json
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.users = []
        self.clients = []

    def Connect(self, request, context):
        user = {'name': request.name, 'peer': context.peer()}
        self.users.append(user)

        print(f"{request.name} conectou-se ao servidor.")
        self.notify_clients(f"{request.name} conectou-se ao servidor.")

        meta = chat_pb2.ServerMeta(server_name=config['name'], motd=config['motd'], max_users=config['max_users'], user_count=(len(self.clients) + 1))
        return meta

    def SendMessage(self, request, context):
        for client in self.clients:
            timestamp = Timestamp()
            timestamp.FromDatetime(datetime.now())
            request.timestamp.CopyFrom(timestamp)
            client.append(request)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.name}: {request.text}")

        return chat_pb2.Empty()
    
    def notify_clients(self, notification_message):
        notification = chat_pb2.ChatMessage(name="Servidor", text=notification_message)
        for client in self.clients:
            client.append(notification)

    def ChatStream(self, request, context):
        client_messages = deque()
        self.clients.append(client_messages)

        try:
            while True:
                if client_messages:
                    message = client_messages.popleft()
                    yield message
        except Exception as e:
            print(f"Cliente desconectado: {e}")
        finally:
            for user in self.users:
                if user['peer'] == context.peer():
                    print(f"{user['name']} saiu do chat.")
                    self.notify_clients(f"{user['name']} saiu do chat.")
                    self.users.remove(user)
                    break

            self.clients.remove(client_messages)
    
    def disconnect_clients(self):
        for client in self.clients:
            client.cancel()
        self.clients.clear()

def serve():
    print("Iniciando servidor de chat...")
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    chat_service = ChatService()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service, server)

    SERVICE_NAMES = (
        chat_pb2.DESCRIPTOR.services_by_name['ChatService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f'[::]:{config["port"]}')
    server.start()

    print(f"Nome do servidor: {config['name']}")
    print(f"Máximo de usuários: {config['max_users']}")
    print(f"Mensagem do dia: {config['motd']}")
    print(f"Servidor de chat iniciado na porta {config['port']}.")
    print("-----------------------------")

    def signal_handler(sig, frame):
        print("Servidor encerrando...")
        stop = server.stop(None)
        stop.wait(5)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    server.wait_for_termination()

if __name__ == '__main__':
    with open('config.json', 'r') as f:
            global config 
            config = json.load(f)

    serve()
