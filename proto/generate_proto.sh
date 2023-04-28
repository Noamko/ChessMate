# python3 -m grpc_tools.protoc  -I. --python_out=../Chessm8/build/proto --grpc_python_out=../Chessm8/build/proto

protoc *.proto --java_out=../android/lichess/app/src/main/java 
# protoc --java_out=../build/proto *.proto
# mkdir ../../board/proto
# protoc --cpp_out=../../board *.proto
