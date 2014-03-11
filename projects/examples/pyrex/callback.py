
def eggs(x,y):
    return x+y


def spam(x,y):
    return x*y


from callback_ext import doit, default_action



class A:
    def __init__(self):
        pass
    
    def __call__(self, x, y):
        return eggs(x,y) + default_action(x,spam(x,y))
    


for func in [eggs, spam, default_action, A()]:
    print doit(func,3,4)

