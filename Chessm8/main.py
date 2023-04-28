"""  Chess8 main file. 
        This file is the main file for the chessm8 project.
        It will be responsible for running the game and 
        communicating with the chess engine & the chess board.

    Basic flow:
        1. Initialize bluetooth connection with Android app (durint )
        2. Initialize ack with chessboard
        3. Initialize chess engine
        4. Wait for commands from Android app
"""
from concurrent import futures
import sys
import grpc
sys.path.append("build/proto")
import server_pb2
import server_pb2_grpc


class HelloWorldServicer(server_pb2_grpc.HelloWorldServicer):
    def SayHello(self, request, context):
        return server_pb2.HelloResponse(message='Hello, %s!' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_HelloWorldServicer_to_server(HelloWorldServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def main():
    serve()

if __name__ == '__main__':
    main()
    