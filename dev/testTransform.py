def transformX(T,B,xT, x1):
    xB=xT*(B/T)
    return x1+xB


x01=transformX(T=10, B=5, xT=4, x1=10)
print(x01)