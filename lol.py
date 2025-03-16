def mygen(var):
    print(var)
    while True:
        var2 = yield
        print(var + var2)

a = mygen(3)
a.send(None)
a.send(5)
a.send(5)
a.send(5)
a.send(5)