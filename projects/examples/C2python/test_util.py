import util_ext

print dir(util_ext)

util_ext.hello('Hello World')

print 'Precision', util_ext.double_precision()
        
x0 = 5.0; y0 = 5.0; z0 = 10.0
x1 = 8.0; y1 = 2.0; z1 = 1.0


a, b = util_ext.gradient(x0, y0, x1, y1, z0, z1)
print 'gradient', a, b


