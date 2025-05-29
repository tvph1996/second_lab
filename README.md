This project aims to analyze the difference in performance between gRPC and REST.\\

The gRPC-server is realized based on the lab content. To build and run it in Docker:\
```docker build -t server_grpc ./server_grpc```\
```docker run -p 50051:50051 server_grpc```\

The REST-server is rebuilt from the first lab using FastAPI as Flask have heavy overhead. Run it in Docker:\
```docker build -t server_rest ./server_rest```\
```docker run -p 8000:8000 server_rest```

some contents in protobuf, gRPC-server are different compared to lab guideline during the implementation.\

gRPC source files is compiled locally.\

there are 2 clients, one is to test the gRPC-server, one is for the performance test.\

performance test logs, data table and the lab report together with all necessary source files are presented\
