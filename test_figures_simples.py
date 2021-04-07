import numpy as np
import xlrd
from math import *
import matplotlib.pyplot as plt
from matplotlib import animation

def creer_contour_carre(n):
    A=np.zeros((n,n))
    indices_i=[]
    indices_j=[]
    for i in range(10,n-10):
        A[i,10]=1
        indices_i.append(i)
        indices_j.append(10)
        A[10,i]=1
        indices_i.append(10)
        indices_j.append(i)
        A[n-11,i]=1
        indices_i.append(n-11)
        indices_j.append(i)
        A[i,n-11]=1
        indices_i.append(i)
        indices_j.append(n-11)
    return(A,indices_i,indices_j)

def creer_contour_cercle(n):
    A=np.zeros((n,n))
    indices_i=[]
    indices_j=[]
    for i in range(n):
        for j in range(n):
            d=sqrt((i-(n//2))**2+(j-(n//2))**2)
            if d>=n/2-5 and d<=n/2-2 :
                A[i,j]=1
                indices_i.append(i)
                indices_j.append(j)
    return(A,indices_i,indices_j)

def gradient(i,j,indices_i,indices_j):
    grad_i=(sqrt(distance_cotes(int(i)+1,int(j),indices_i,indices_j))-sqrt(distance_cotes(int(i)-1,int(j),indices_i,indices_j)))/2
    grad_j=(sqrt(distance_cotes(int(i),int(j)+1,indices_i,indices_j))-sqrt(distance_cotes(int(i),int(j)-1,indices_i,indices_j)))/2
    return(grad_i,grad_j)

def distance_cotes(i,j,indices_i,indices_j):
    N=len(indices_i)
    d=(indices_i[0]-i)**2+(indices_j[0]-j)**2
    for k in range(1,N):
        d=min(d,(indices_i[k]-i)**2+(indices_j[k]-j)**2)
    return(d)

def matrice_avec_le_point(i,j,n): #cette fonction donne une matrice nulle partout sauf au point (i,j)
    B=np.zeros((n,n))
    B[int(i),int(j)]=5
    return(B)

def nemo_gradient(n,i,j,pas_deplac): #calcule le point nemo a l'aide de la méthode du gradient / n : le pas de la discretisation / i,j : indices du point de depart / k : pas du deplacement du point
    i=(i*n)//2
    j=(j*n)//2
    C,indices_i,indices_j=creer_contour_cercle(n)
    fig=plt.figure()
    ims=[[plt.imshow(C,animated=True)]]
    liste=[]
    for k in range(250):
        gi,gj=gradient(i,j,indices_i,indices_j)
        liste.append((gi,gj))
        #print("k=",k,"gi=",gi,"gj=",gj)
        if (i+(gi/pas_deplac))<n and (i+(gi/pas_deplac))>0 : i+=(gi/pas_deplac)
        if (j+(gj/pas_deplac))<n and (j+(gj/pas_deplac))>0 : j+=(gj/pas_deplac)        
        ims.append([plt.imshow(C+matrice_avec_le_point(i,j,n),animated=True)])

    ani=animation.ArtistAnimation(fig,ims,interval=50,blit=True,repeat_delay=5)

    plt.show()
    return(liste)

def matrice_des_gradients(n):
    C,indices_i,indices_j=creer_contour_cercle(n)
    G=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            #gi,gj=gradient(i,j,indices_i,indices_j)
            #G[i,j]=gi**2 + gj**2
            G[i,j]=distance_cotes(i,j,indices_i,indices_j)
    plt.imshow(G)
    plt.show()
