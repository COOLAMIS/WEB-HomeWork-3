from time import time
from multiprocessing import cpu_count, Process

result = []
a = 128
b = 255
c = 99999
d = 10651060
number = a
def factorize():
    num = 1
    while True:
        if number%num == 0:
            result.append(num)
        num += 1
        if num > number:
            break
    return print(result)

if __name__ == '__main__':
    sum_cpu = cpu_count()
    t = time()
    for i in range(sum_cpu):
        pr = Process(target=factorize)
        pr.start()
    print(time() - t)
    
