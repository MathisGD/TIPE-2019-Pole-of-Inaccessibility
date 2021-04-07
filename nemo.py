import matplotlib.pyplot as plt
from math import *
import numpy
from random import randint
import matplotlib.image as mpimg
import sys

def distance(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def dmin(C,a):
    dmin=distance(a,(0,0))
    for i in range (len(C)):
        for j in range (len(C[0])):
            if C[i][j]==1:
                dij=distance(a,(i,j))
                if dij<dmin: dmin=dij
    return(dmin)

def maxi (C,l) :
    x,y,dnem=0,0,l[0][0]
    lretour=[(0,0)]
    for i in range (len(C)):
        for j in range(len(C[0])):
            if l[i][j]>dnem :
                dnem=l[i][j]
                lretour=[]
            if l[i][j]==dnem : lretour.append((i,j))
    return (lretour)
    
def aux (C,x,y,l):
    if l[x][y]==-1 :
        l[x][y]=dmin(C,(x,y))
        if C[x+1][y] != 1 : aux (C,x+1,y,l)
        if C[x-1][y] != 1 : aux (C,x-1,y,l)
        if C[x][y-1] != 1 : aux (C,x,y-1,l)
        if C[x][y+1] != 1 : aux (C,x,y+1,l)

def solve(C,x,y):
    l=[[-1 for k in range (len(C))] for k in range (len(C[0]))]
    aux(C,x,y,l)#fonction à effet de bord !!!
    listeNemo=maxi(C,l)
    for k in listeNemo :
        x,y=k
        C[x][y]=3

def contour1(M):
    n=len(M)
    C=numpy.zeros((n,n),dtype=int)
    Done=numpy.zeros((n,n),dtype=bool)
    
    def aux(x,y):
        if not(Done[x][y]) :
            Done[x][y]=True
            if M[x][y]==0 :
                C[x][y]=1
                if x<n-1:
                    #if M[x+1][y]==1 : C[x][y]=2
                    aux(x+1,y) #bas
                if x>0:
                    #if M[x-1][y]==1 : C[x][y]=2
                    aux(x-1,y) #haut
                if y<n-1:
                    #if M[x][y+1]==1 : C[x][y]=2
                    aux(x,y+1) #droite
                if y>0:
                    #if M[x][y-1]==1 : C[x][y]=2
                    aux(x,y-1) #gauche
    aux(0,0)
    return(C)

def contour2(M):
    n=len(M)
    file=[(0,0)]
    visite=numpy.zeros((n,n),dtype=bool)
    C=numpy.zeros((n,n),dtype=int)
    while file!=[] :
        (x,y)=file[0]
        del file[0]
        if not (visite[x][y]) :
            if M[x][y]==0:
                C[x][y]=1
                visite[x][y]=True
                if x<n-1: file.append((x+1,y)) #bas
                if x>0: file.append((x-1,y)) #haut
                if y<n-1: file.append((x,y+1)) #droite
                if y>0: file.append((x,y-1)) #gauche
    return C

def figure_alea(n):
    M=numpy.zeros((n,n),dtype=int)
    M=numpy.array(M)
    i=int(n/2)
    j=int(n/2)
    M[i][j]=1
    for k in range(40*n):
        a=randint(1,4)
        if a==1 and j<n-2: #droite
            j+=1
            M[i][j]=1
        elif a==2 and j>1: #gauche
            j-=1
            M[i][j]=1
        elif a==3 and i>1: #haut
            i-=1
            M[i][j]=1
        elif a==4 and i<n-2: #bas
            i+=1
            M[i][j]=1
    return(M)

def affiche1(n):
    sys.setrecursionlimit(n*n+1)
    for k in range(1):
        M=figure_alea(n)
        C=contour1(M)
        solve(C,int(n/2),int(n/2))
        plt.imshow(C)
        plt.show()

def affiche2(n):
    sys.setrecursionlimit(n*n+1)
    for k in range(1):
        M=figure_alea(n)
        C=contour2(M)
        solve(C,int(n/2),int(n/2))
        plt.imshow(C)
        plt.show()


