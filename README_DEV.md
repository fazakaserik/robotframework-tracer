# Compile .proto

`python -m grpc_tools.protoc -I .\src\proto --python_out=.\src --pyi_out=.\src --grpc_python_out=.\src .\src\proto\display.proto`