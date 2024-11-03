import grpc
import server_pb2
import server_pb2_grpc
import threading

def send_message(stub, username):
    while True:
        text = input(f"{username}: ")
        if text.lower() == 'exit':
            break
        message = server_pb2.ChatMessage(name=username, text=text)
        stub.SendMessage(message)

def receive_messages(stub):
    try:
        for chat_message in stub.ChatStream(server_pb2.Empty()):
            print(f"\n{chat_message.name}: {chat_message.text}")
    except grpc.RpcError as e:
        print(f"Error receiving messages: {e}")

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = server_pb2_grpc.ChatServiceStub(channel)

    username = input("Enter your username: ")

    receive_thread = threading.Thread(target=receive_messages, args=(stub,))
    receive_thread.start()

    send_message(stub, username)

    receive_thread.join()
    print("You have exited the chat.")

if __name__ == '__main__':
    main()
