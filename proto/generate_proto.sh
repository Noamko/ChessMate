mkdir -p ../Chessm8/build/proto
python3 -m grpc_tools.protoc  -I. *.proto --python_out=../Chessm8/build/proto --grpc_python_out=../Chessm8/build/proto
