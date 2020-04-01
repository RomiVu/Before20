import socket

port = 1000
address = None
family = socket.AF_UNSPEC
flags = socket.AI_PASSIVE


for res in sorted(
        socket.getaddrinfo(address, port, family, socket.SOCK_STREAM, 0, flags),
        key=lambda x: x[0]
    ):
    af, socktype, proto, canonname, sockaddr = res
    print(af, socktype, proto, canonname, sockaddr)
