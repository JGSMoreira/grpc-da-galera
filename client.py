import grpc
import chat_pb2
import chat_pb2_grpc
import threading
from collections import deque
import os

msgs = deque()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_messages():
    clear()
    for msg in msgs:
        print(f"[{msg.name}]: {msg.text}")

def send_message(stub, username):
    while True:
        text = input(f"> ")

        # Validações
        if text == '':
            show_messages()
            continue

        # Comandos
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
        print(f"Erro ao receber mensagens: {e}")

def main():
    ip = input("Digite o IP do servidor de chat: ")
    ip = f'{ip}:50051' if ip != '' else 'localhost:50051'

    channel = grpc.insecure_channel(ip)
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    username = input("Digite seu nome de usuário: ")

    receive_thread = threading.Thread(target=receive_messages, args=(stub,))
    receive_thread.start()

    send_message(stub, username)

    receive_thread.join()
    print("Você saiu do chat.")

if __name__ == '__main__':
    main()
