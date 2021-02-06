keys = "xyz"
indexs = range(3)

value = 0;


def gv():
    global value
    value = value + 1
    print(f'{value},')


def k(*args):
    print('{')
    for key in keys:
        print(f'"{key}":')
        if args:
            args[0](*(args[1:]))
        else:
            gv()
    print('},')


def a(*args):
    print('[')
    for index in indexs:
        if args:
            args[0](*(args[1:]))
        else:
            gv()
    print('],')


def data(*args):
    p = args[0]
    c = args[1:]
    p(*c)


#data(a, k, k, a, k, k, k, a)
#data(k, a, a, k, a, a, a, k)
# data(k,k,k)
data(a, a, a)
