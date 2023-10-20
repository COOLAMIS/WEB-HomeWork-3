from time import time

result = []
a = 128
b = 255
c = 99999
d = 10651060

def factorize(number):
    num = 1
    while True:
        if number%num == 0:
            result.append(num)
        num += 1
        if num > number:
            break
    return result
    
t = time()
print(factorize(a))
print(time() - t)


