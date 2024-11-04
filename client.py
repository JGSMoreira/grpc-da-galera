import grpc
import chat_pb2
import chat_pb2_grpc
import threading
from collections import deque
import os
import sys
import signal

msgs = deque()
username = ''

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_mensagens():
    limpar()
    mostrar_metadados_servidor()
    for msg in msgs:
        timestamp = msg.timestamp.ToDatetime().strftime('%H:%M:%S')
        print(f"[{timestamp}] {msg.name}: {msg.text}")
        
    print(f"{username}> ", end='', flush=True)

def enviar_mensagem(stub):
    while True:
        text = input()

        if text.lower() == '/sair':
            print("Desconectando do servidor...")
            channel.close()
            break 

        if text == '/limpar':
            msgs.clear()
            limpar()
            continue

        message = chat_pb2.ChatMessage(name=username, text=text)
        stub.SendMessage(message)

def receber_mensagens(stub):
    try:
        for chat_message in stub.ChatStream(chat_pb2.Empty()):
            msgs.append(chat_message)
            mostrar_mensagens()
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.CANCELLED:
            print(f"\nErro ao receber mensagens: {e.details()}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

def mostrar_metadados_servidor():
    print("------ Informações do servidor ------")
    print(f"Servidor: {server_meta.server_name}")
    print(f"Usuários conectados: {server_meta.user_count}/{server_meta.max_users}")
    print(f"{server_meta.motd}")
    print("-------------------------------------")

def conectar():
    ip = input("\nDigite o IP do servidor de chat que deseja se conectar: ")
    ip = f'{ip}' if ip != '' else 'localhost:50051'

    global channel
    channel = grpc.insecure_channel(ip)
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    limpar()

    global username
    username = input("\nDigite seu nome de usuário: ")
    try:
        print(f"Conectando ao servidor de chat com IP {ip}...")
        connect_request = chat_pb2.ConnectRequest(name=username)
        global server_meta 
        server_meta = stub.Connect(connect_request)
        mostrar_metadados_servidor()
    except grpc.RpcError as e:
            print(f"\nErro ao conectar ao servidor: {e.details()}")
            return

    receive_thread = threading.Thread(target=receber_mensagens, args=(stub,), daemon=True)
    receive_thread.start()

    enviar_mensagem(stub)

def main():
    while True:
        print("Cliente Parichatt")
        try:
            conectar()
        except grpc.RpcError as e:
            print(f"\nErro ao conectar ao servidor: {e.details()}")
            continue
        
        def signal_handler(sig, frame):
            print("\nDesconectando do servidor...")
            channel.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        

if __name__ == '__main__':
    main()
