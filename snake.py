import time
import random
import sys
import os
#import keyboard
from math import trunc

def cl(F):
    for i in range(1, 19):
        for j in range(1, 19):
            F[i][j] = '_'

def get_point(S):
    g = len(S)
    p = random.randint(0, 18 * 18 - 1 - g)
    for i in range(1, 19):
        for j in range(1, 19):
            if [j, i] not in S:
                if p == 0:
                    return [i, j]
                else:
                    p -= 1
def init():
    F = [['_' for i in range(20)] for j in range(20)]
    for i in range(20):
        F[0][i] = '$'
        F[i][0] = '$'
        F[19][19 - i] = '$'
        F[19 - i][19] = '$'
    h = [random.randint(2, 18), random.randint(2, 18)]
    d = 'l'
    m = h[0] - 1
    S = [h]
    if 20 - h[0] > m:
        d = 'r'
        m = 20 - h[0]
    if h[1] - 1 > m:
        d = 'u'
        m = h[1] - 1
    if 20 - h[1] > m:
        d = 'd'
        m = 20 - h[1]
    if d == 'l':
        S.append([h[0] + 1, h[1]])
    elif d == 'r':
        S.append([h[0] - 1, h[1]])
    elif d == 'u':
        S.append([h[0], h[1] + 1])
    else:
        S.append([h[0], h[1] - 1])
    cl(F)
    p = get_point(S)
    for i in S[1:]:
        F[i[1]][i[0]] = '#'
    F[S[0][1]][S[0][0]] = '@'
    F[p[0]][p[1]] = '*'
    return F, S, d, h, p

        
def step(F, S, d, h, p):
    if 1:
        cl(F)
        if d == 'l':
            h = [h[0] - 1, h[1]]
        elif d == 'r':
            h = [h[0] + 1, h[1]]
        elif d == 'u':
            h = [h[0], h[1] - 1]
        elif d == 'd':
            h = [h[0], h[1] + 1]
        S.insert(0, h)
        del(S[-1])
        for i in S[1:]:
            F[i[1]][i[0]] = '#'
        F[p[0]][p[1]] = '*'
        F[S[0][1]][S[0][0]] = '@'
        if S[0][1] == p[0] and S[0][0] == p[1]:
            S.append(S[-1])
            p = get_point(S[:-1])
            F[p[0]][p[1]] = '*'
            """
        for i in F:
            for j in i:
                print(j, end = '')
            print('')
            """
        x, y = h
        if h in S[4:]:
            return (False, F, S, d, h, p)
        if x == 0 or x == 19 or y == 0 or y == 19:
            return (False, F, S, d, h, p)
        
        return (True, F, S, d, h, p)

"""
F = [[' ' for i in range(20)] for j in range(20)]
for i in range(20):
    F[0][i] = '$'
    F[i][0] = '$'
    F[19][19 - i] = '$'
    F[19 - i][19] = '$'
h = [random.randint(2, 18), random.randint(2, 18)]
d = 'l'
m = h[0] - 1
S = [h]
if 20 - h[0] > m:
    d = 'r'
    m = 20 - h[0]
if h[1] - 1 > m:
    d = 'u'
    m = h[1] - 1
if 20 - h[1] > m:
    d = 'd'
    m = 20 - h[1]
if d == 'l':
    S.append([h[0] + 1, h[1]])
elif d == 'r':
    S.append([h[0] - 1, h[1]])
elif d == 'u':
    S.append([h[0], h[1] + 1])
else:
    S.append([h[0], h[1] - 1])
p = get_point(S)
t = trunc(time.clock())
tr = 1
cl(F)
for i in S[1:]:
    F[i[1]][i[0]] = '#'
F[S[0][1]][S[0][0]] = '@'
F[p[0]][p[1]] = '*'
for i in F:
    for j in i:
        print(j, end = '')
    print('')
if d == 'l':
    h = [h[0] - 1, h[1]]
elif d == 'r':
    h = [h[0] + 1, h[1]]
elif d == 'u':
    h = [h[0], h[1] - 1]
elif d == 'd':
    h = [h[0], h[1] + 1]
S.insert(0, h)
del(S[-1])
x, y = h
if x == 1 or x == 19 or y == 1 or y == 19:
    tr = 0
    kk = 1
while tr:
    tt = trunc(time.clock() * 10)
    h = S[0]
    if keyboard.is_pressed('w') and kk and d != 'd': 
        d = 'u'
        kk = 0
    elif keyboard.is_pressed('s') and kk and d != 'u':
        d = 'd'
        kk = 0
    elif keyboard.is_pressed('a') and kk and d != 'r':
        d = 'l'
        kk = 0
    elif keyboard.is_pressed('d') and kk and d != 'l':
        d = 'r'
        kk = 0
    else:
        pass
    
    if tt > t:
        kk = 1
        t += 1
        cl(F)
        if d == 'l':
            h = [h[0] - 1, h[1]]
        elif d == 'r':
            h = [h[0] + 1, h[1]]
        elif d == 'u':
            h = [h[0], h[1] - 1]
        elif d == 'd':
            h = [h[0], h[1] + 1]
        S.insert(0, h)
        del(S[-1])
        for i in S[1:]:
            F[i[1]][i[0]] = '#'
        F[p[0]][p[1]] = '*'
        F[S[0][1]][S[0][0]] = '@'
        if S[0][1] == p[0] and S[0][0] == p[1]:
            S.append(S[-1])
            p = get_point(S[:-1])
            F[p[0]][p[1]] = '*'
        for i in F:
            for j in i:
                print(j, end = '')
            print('')
        x, y = h
        if h in S[4:]:
            break
        if x == 0 or x == 19 or y == 0 or y == 19:
            break
"""
