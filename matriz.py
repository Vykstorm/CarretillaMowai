#!/usr/bin/python
  # -*- coding: iso8859-1 -*-
# DescripciÃ³n:
# Este script define una representación de una matriz.


class matriz:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.valores = [0] * (n*m)
    def get_rows(self):
        return self.n
    
    def get_cols(self):
        return self.m

    def get(self, i,j):
        return self.valores[self.m * i + j]

    def set(self, i,j, x):
        self.valores[self.m * i + j] = x

    def __getitem__(self, indexes):
        i, j = indexes
        return self.get(i,j)
    def __setitem__(self, indexes, x):
        i, j = indexes
        self.set(i,j,x)

    def __str__(self):
        s = ''
        for i in range(0,self.n):
            for j in range(0,self.m):
                s = s + repr(self.get(i,j)).ljust(10)
            s = s + '\n'
        return s
