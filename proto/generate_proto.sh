mkdir -p ../cm_server/build/proto
python3 -m grpc_tools.protoc  -I. *.proto --python_out=../server/build/proto --grpc_python_out=../server/build/proto
cp  ./*.proto ../android/chessmate/app/src/main/proto/

