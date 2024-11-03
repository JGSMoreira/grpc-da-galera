import grpc
import server_pb2
import server_pb2_grpc
from concurrent.futures import ThreadPoolExecutor
from grpc_reflection.v1alpha import reflection
from collections import deque

class ChatService(server_pb2_grpc.ChatServiceServicer):
    def __init__(self):

        self.clients = []

    def SendMessage(self, request, context):
        for client in self.clients:
            client.append(request)
        print(f"Received message from {request.name}: {request.text}")
        return server_pb2.Empty()

    def ChatStream(self, request, context):
        client_messages = deque()
        self.clients.append(client_messages)

        try:
            while True:
                if client_messages:
                    message = client_messages.popleft()
                    yield message
        except Exception as e:
            print(f"Client disconnected: {e}")
        finally:
            self.clients.remove(client_messages)

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)

    SERVICE_NAMES = (
        server_pb2.DESCRIPTOR.services_by_name['ChatService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Chat server is running on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()