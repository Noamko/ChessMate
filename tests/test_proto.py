# create a grpc client
import unittest
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/build/proto")
print(f"{os.getcwd()}/build/proto")
sys.path.append("../build/proto")
import grpc
import message_pb2
import message_pb2_grpc
import time

class TestProto(unittest.TestCase):
    # init grpc server for testing

    def setUp(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.commandStub = message_pb2_grpc.CommandStub(channel)

    def test_challenge_ai(self):
        # Create the request
        request = message_pb2.CommandRequest()
        request.name = "ChallengeAI"
        request.challengeAI.level = 1

        # Send the request
        response = self.commandStub.Execute(request)
        
        print(response)


if __name__ == '__main__':
    unittest.main()