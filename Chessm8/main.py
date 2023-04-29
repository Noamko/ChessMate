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
import helloworld_pb2
import helloworld_pb2_grpc

class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("hello")
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("go")
    server.start()
    server.wait_for_termination()

def main():
    print("starting grpc server")
    serve()

if __name__ == '__main__':
    main()
    