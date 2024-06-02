from symtable import Symbol
import math


class node:
    def __init__(self):
        self.sym = ''
        self.pro = 0.0
        self.arr = [0]*20
        self.top = 0


p = [node() for _ in range(20)]


def shannon(l, h, p):
    pack1 = 0
    pack2 = 0
    diff1 = 0
    diff2 = 0
    if (l + 1) == h or l == h or l > h:
        if l == h or l > h:
            return
        p[h].top += 1
        p[h].arr[p[h].top] = 0
        p[l].top += 1
        p[l].arr[p[l].top] = 1

        return

    else:
        for i in range(l, h):
            pack1 = pack1 + p[i].pro
        pack2 = pack2 + p[h].pro
        diff1 = pack1 - pack2
        if diff1 < 0:
            diff1 = diff1 * -1
        j = 2
        while j != h - l + 1:
            k = h - j
            pack1 = pack2 = 0
            for i in range(l, k+1):
                pack1 = pack1 + p[i].pro
            for i in range(h, k, -1):
                pack2 = pack2 + p[i].pro
            diff2 = pack1 - pack2
            if diff2 < 0:
                diff2 = diff2 * -1
            if diff2 >= diff1:
                break
            diff1 = diff2
            j += 1

        k += 1
        for i in range(l, k+1):
            p[i].top += 1
            p[i].arr[p[i].top] = 1

        for i in range(k + 1, h+1):
            p[i].top += 1
            p[i].arr[p[i].top] = 0

        shannon(l, k, p)
        shannon(k + 1, h, p)


def sortByProbability(n, p):
    temp = node()
    for j in range(1, n):
        for i in range(n - 1):
            if p[i].pro > p[i + 1].pro:
                temp.pro = p[i].pro
                temp.sym = p[i].sym

                p[i].pro = p[i + 1].pro
                p[i].sym = p[i + 1].sym

                p[i + 1].pro = temp.pro
                p[i + 1].sym = temp.sym


global dataLen
dataLen = {}


def display(n, p):
    print("\n\nSymbol\tProbability\tCode", end='')
    for i in range(n - 1, -1, -1):
        print("\n", p[i].sym, "\t", p[i].pro, "\t\t", end='')
        for j in range(p[i].top+1):
            print(p[i].arr[j], end='')
            dataLen[p[i].sym] = p[i].top+1


def calculateEntropy(n, p):
    entropy = 0.0
    for i in range(n):
        entropy = entropy + (p[i].pro * math.log2(1 / p[i].pro))
    return round(entropy, 3)


def averageCodeLength(data, p):
    x = []
    for i in dataLen.values():
        x.append(i)
    x.reverse()
    codeLength = 0
    for i in range(len(x)):
        codeLength = codeLength + (p[i].pro * x[i])
    return codeLength


def calculateCodeEfficiency(entropy, codeLength):
    codeEfficiency = (entropy / codeLength)*100
    return round(codeEfficiency, 3)


total = 0
data = []
n = int(input("\n\nEnter the number of symbols: "))

for i in range(0, n):
    p[i].sym = 's' + str(i+1)
    print("Enter the probability of", p[i].sym, ": ", end='')
    probability = float(input())
    data.append(probability)
    assert(probability >= 0.0 and probability <= 1.0)


for i in range(n):
    p[i].pro = data[i]
    total = total + p[i].pro

    if (total > 1):
        print("Invalid. Enter new values")
        total = total - p[i].pro
        i -= 1

i += 1
p[i].pro = 1 - total
sortByProbability(n, p)

for i in range(n):
    p[i].top = -1

shannon(0, n - 1, p)
display(n, p)

print("\n\nShannon Fano Entropy is: ", calculateEntropy(n, p))
print("\nAverage Code Length is: ", averageCodeLength(data, p))
print("\nCode Efficiency is: ", calculateCodeEfficiency(
    calculateEntropy(n, p), averageCodeLength(data, p)), "%\n\n")