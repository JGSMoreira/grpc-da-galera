# grpc-da-galera

Este é um aplicativo de chat simples utilizando gRPC para comunicação cliente/servidor. O servidor permite que múltiplos clientes se conectem e troquem mensagens em tempo real.

## Arquitetura

A aplicação é composta por dois componentes principais:

1. **Servidor gRPC**: Implementado na classe `ChatService`, que gerencia a conexão e troca de mensagens entre os clientes.
2. **Cliente**: Permite ao usuário enviar e receber mensagens através do terminal.

### Funcionamento do gRPC

gRPC é um sistema de chamada de procedimento remoto (RPC) que usa HTTP/2 para transporte, permitindo comunicação eficiente entre serviços. O protocolo é baseado em Protobuf (Protocol Buffers), que define as mensagens e serviços utilizados pela aplicação.

O serviço de chat é definido no arquivo `chat.proto`, que especifica as mensagens que podem ser enviadas e os métodos disponíveis. As mensagens são serializadas para serem enviadas através da rede e deserializadas ao serem recebidas.

## Requisitos

- Python 3.6 ou superior
- Dependências listadas no arquivo "requirements.txt"

## Instalação

1. Clone o repositório:
   ```bash
   git clone <https://github.com/JGSMoreira/grpc-da-galera>

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

3. Compile o arquivo Protobuf:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

## Execução

1. Inicie o cliente: em outro terminal, execute:
    ```bash
   python server.py

2. Inicie o servidor: No terminal, execute:
    ```bash
   python client.py

## Como usar

- Após executar os comandos no terminal, crie um nove de usuário;
- Os usuários podem se conectar ao servidor e enviar mensagens uns aos outros em tempo real;
- As mensagens enviadas são exibidas no terminal do cliente, e os usuários podem ver o que outros estão enviando.
  
