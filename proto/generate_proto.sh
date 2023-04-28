# python3 -m grpc_tools.protoc  -I. --python_out=../Chessm8/build/proto --grpc_python_out=../Chessm8/build/proto

protoc *.proto --plugin=protoc-gen-grpc-java=/usr/local/bin/protoc-gen-grpc-java --java_out=./android/app/src/main/java --grpc-java_out=./andorid/app/src/main/java 
# protoc --java_out=../build/proto *.proto
# mkdir ../../board/proto
# protoc --cpp_out=../../board *.proto
