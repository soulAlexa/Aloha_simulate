import random
import asyncio
import numpy
from matplotlib import pyplot as plt
import math
import scipy
LENG = 100000


def Aloha(lamb, p, m, flag, time):
    if lamb <= .0:
        lamb = .001
    outN = 0.0
    outC = 0.0
    outT = 0.0
    lambM = lamb/m
    Userlate = [[] for i in range(m)]
    curi = 0
    # while curi < time:
    while True:
        poison = scipy.stats.poisson.rvs(mu=lambM, size=m)
        activ = -1
        if curi < time:
            for i in range(0, m, 1):
                for j in range(poison[i]):
                    Userlate[i].append(curi)
        for i in range(0, m, 1):
            if Userlate[i] and Userlate[i][0] < curi:
                if (flag and curi - Userlate[i][0] == 1) or random.random() < p:
                    if activ < 0:
                        activ = i
                    else:
                        activ = -1
                        break
        if activ >= 0:
            outC += 1
            outT += curi - Userlate[activ][0]
            outN += curi - Userlate[activ][0] - 1
            Userlate[activ].pop(0)
        curi += 1
        k = 0
        for i in range(0, m, 1):
            if Userlate[i]:
                k = 1
                break
        # print(curi, k, m, lamb)
        if curi >= time and k == 0:
            break
    return outN/curi, outT/outC, outC/curi


def alohaprint(time, m, p, flag, subN):
    mass1 = [[] for i in range(len(m))]
    mass2 = [[] for i in range(len(m))]
    mass3 = [[] for i in range(len(m))]
    massLamb = numpy.arange(0.1, 1, 0.1)
    for i in range(len(massLamb)):
        for ii in range(len(m)):
            # print( 1/m[ii])
            n, d, lam = Aloha(massLamb[i], p, m[ii], flag, time)
            mass1[ii].append(n)
            mass2[ii].append(d)
            mass3[ii].append(lam)
    print(mass2)
    s = []
    for i in m:
        # s.append(f'm={i},Flag={flag}, p = {p}')
        s.append(f'm={i},p = {p}')
    # print(mass1)
    # print(massLamb)
    drawArrays(massLamb, mass1, sub=subN, linesLabel=s)#средкол аб
    drawArrays(massLamb, mass2, sub=subN + 1, linesLabel=s)#сред задержка
    drawArrays(massLamb, mass3, sub=subN + 2, linesLabel=s)#интенсивность вход потока
    # plt.show()


def drawArrays(x, ys, lineType='-', xL='', yL='', linesLabel=None, fillIt=False, sub=0):
    if sub != 0:
        plt.subplot(sub)

    if linesLabel is None:
        for y in ys:
            plt.plot(x, y, lineType)
            if fillIt:
                plt.fill_between(x, y)
    else:
        i = 0
        for y in ys:
            plt.plot(x, y, lineType, label=linesLabel[i])
            if fillIt:
                plt.fill_between(x, y)
            i += 1
        plt.legend()

    plt.ylabel(yL)
    plt.xlabel(xL)
    plt.grid(visible=True)

def synkh_chanel(labm):
    if labm <= .0:
        labm = .001
    all_times = 0.0
    q = 0.0
    mass = []
    counter = 0.0
    timer = 0.0
    for i in range(0, LENG):
        counter += -numpy.log(random.random())/labm
        if timer < counter:
            timer = numpy.ceil(counter)
        timer += 1
        mass.append((counter, timer))
        all_times += timer - counter
        q += numpy.floor(timer-counter)
    # print(mass)
    print(q/timer, all_times/LENG)
    return q/timer, all_times/LENG

def asynkh_channel(labm):
    if labm <= .0:
        labm = .001
    all_times = 0.0
    q = 0.0
    counter = 0.0
    timer = 0.0
    for i in range(0, LENG):
        counter += -numpy.log(random.random())/labm
        if timer < counter:
            timer = counter
        timer += 1
        all_times += timer - counter
        q += numpy.floor(numpy.ceil(timer)-counter)
    return q/timer, all_times/LENG

def graf6():
    mass = [[], [], []]
    mass2 = [[], [], [], []]
    mass3 = numpy.arange(0, 1, 0.1)
    for i, x in enumerate(range(0, 10, 1)):
        x = x/10
        # x = x*2
        n1, d1 = synkh_chanel(x)#синронный канал
        n2, d2 = asynkh_channel(x)#асинхронный

        mass[0].append(x * (2 - x) / (2 * (1 - x)))
        mass[1].append(n1)
        mass[2].append(n2)

        mass2[0].append(1.5 if not x else mass[0][i] / x + .5)
        mass2[1].append(d1)
        mass2[2].append(1. if not x else mass[0][i] / x)
        mass2[3].append(d2)
    drawArrays(mass3, mass, sub=121, xL="lam", yL="N(lam)", linesLabel=["Теоритическое", "Синхронная", "Асинхронная"])
    drawArrays(mass3, mass2, sub=122, xL="lam", yL="d(lam)", linesLabel=["Синхронная теоритическое", "Синхронная моделированное", "Асинхронная теоритическое", "Асинхронная моделированное"])
    plt.show()

if __name__ == '__main__':
    # graf6()
    # print(synkh_chanel(22))
    # alohaprint(20000, [1], 0.1, True, 131)
    alohaprint(20000, [2, 4, 8, 10, 16], 0.1, False, 231)
    alohaprint(20000, [2, 4, 8, 10, 16], 0.1, True, 234)
    # alohaprint(10000, [1, 2], 0.1, False, 131)

    # for i in range(1, 9, 1):
    #     p = i/10
    #     alohaprint(10000, [4], p, False, 131)
    # for i in range(1, 9, 1):
    #     p = i / 10
    #     alohaprint(10000, [8], p, False, 334)
    # for i in range(1, 9, 1):
    #     p = i / 10
    #     alohaprint(10000, [16], p, False, 337)
    # plt.show()
    # 'хорошее описание, сравнение систем'
    # print(Aloha(0.2, 0.3, 16, 0, 10000))
    # print(Aloha(0.2, 0.3, 16, 0, 10000))
    # f = scipy.stats.poisson.rvs(mu=0.8, size=18)
    # print(f)
