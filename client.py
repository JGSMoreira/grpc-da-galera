import grpc
import chat_pb2
import chat_pb2_grpc
import threading
from collections import deque
import os
import sys

msgs = deque()
username = ''

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_messages():
    clear()
    show_server_meta()
    for msg in msgs:
        timestamp = msg.timestamp.ToDatetime().strftime('%H:%M:%S')
        print(f"[{timestamp}] {msg.name}: {msg.text}")
        
    print(f"{username}> ", end='', flush=True)

def send_message(stub):
    while True:
        text = input()

        if text.lower() == '/sair':
            break 

        if text == '/limpar':
            msgs.clear()
            clear()
            continue

        message = chat_pb2.ChatMessage(name=username, text=text)
        stub.SendMessage(message)

def receive_messages(stub):
    try:
        for chat_message in stub.ChatStream(chat_pb2.Empty()):
            msgs.append(chat_message)
            show_messages()
    except grpc.RpcError as e:
        print(f"\nErro ao receber mensagens: {e}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

def show_server_meta():
    print("------ Informações do servidor ------")
    print(f"Servidor: {server_meta.server_name}")
    print(f"Usuários conectados: {server_meta.user_count}/{server_meta.max_users}")
    print(f"{server_meta.motd}")
    print("-------------------------------------")

def main():
    ip = input("Digite o IP do servidor de chat: ")
    ip = f'{ip}:50051' if ip != '' else 'localhost:50051'

    channel = grpc.insecure_channel(ip)
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    clear()

    global username
    username = input("Digite seu nome de usuário: ")
    print(f"Conectando ao servidor de chat com IP {ip}...")

    try:
        connect_request = chat_pb2.ConnectRequest(name=username)
        global server_meta 
        server_meta = stub.Connect(connect_request)
        show_server_meta()
    except grpc.RpcError as e:
        print(f"\nErro ao conectar ao servidor: {e}")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(stub,), daemon=True)
    receive_thread.start()

    send_message(stub)


if __name__ == '__main__':
    main()
