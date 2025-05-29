This project aims to analyze the difference in performance between gRPC and REST.
\
\
The gRPC-server is realized based on the lab content. To build and run it in Docker:\
```docker build -t server_grpc ./server_grpc```\
```docker run -p 50051:50051 server_grpc```

The REST-server is rebuilt from the first lab using FastAPI as Flask have heavy overhead. Run it in Docker:\
```docker build -t server_rest ./server_rest```\
```docker run -p 8000:8000 server_rest```
\
\
Some contents in protobuf, gRPC-server are different compared to the lab guideline during the implementation.
\
\
gRPC source files is compiled locally, to recompile:\
```python -m grpc_tools.protoc --proto_path=. --python_out=./server_grpc --python_out=./ --grpc_python_out=./server_grpc --grpc_python_out=./  ./myitems.proto```
\
\
There are 2 clients, to run the one testing the gRPC-server:\
```python ./client_grpc_features.py```

To run the one testing the performance of gRPC and REST-server:\
```python client_grpc_performance_test.py```
\
\
The data table and logs of the performance test:\
```data.xlsx```\
```performance_comparison_10times_log.txt```\
\
The lab report:\
```report.docx```
