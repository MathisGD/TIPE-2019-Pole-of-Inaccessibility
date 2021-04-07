import numpy as np
import xlrd
from math import *
import matplotlib.pyplot as plt
from matplotlib import animation

def getlist(): # donne les lat et long sous forme d'une liste (les angles sont convertis en radians)
    document = xlrd.open_workbook("E:\TIPE\donnees cotes\golfe_du_mex.xls")

    #print("Nombre de feuilles: "+str(document.nsheets))
    #print("Noms des feuilles: "+str(document.sheet_names()))
    feuille_1 = document.sheet_by_index(0)
    feuille_1 = document.sheet_by_name("Feuille1")
    #print("Format de la feuille 1:")
    #print("Nom: "+str(feuille_1.name))
    #print("Nombre de lignes: "+str(feuille_1.nrows))
    #print("Nombre de colonnes: "+str(feuille_1.ncols))
    cols = feuille_1.ncols
    rows = feuille_1.nrows

    lat=[radians(float(feuille_1.cell_value(rowx=1, colx=2)))]
    long=[radians(float(feuille_1.cell_value(rowx=1, colx=3)))]

    latmin=lat[0]
    latmax=lat[0]
    longmin=long[0]
    longmax=long[0]

    for k in range (2,rows):
        lat.append(radians(float(feuille_1.cell_value(rowx=k, colx=2))))
        long.append(radians(float(feuille_1.cell_value(rowx=k, colx=3))))
        if lat[-1]<latmin : latmin=lat[-1]
        if lat[-1]>latmax : latmax=lat[-1]
        if long[-1]<longmin : longmin=long[-1]
        if long[-1]>longmax : longmax=long[-1]

    return(latmin,latmax,longmin,longmax,lat,long)

def distance(lat1,long1,lat2,long2): # renvoie la distance spherique de deux points
    r=cos(lat1)*cos(lat2)*cos(long1-long2)+sin(lat1)*sin(lat2)
    if abs(r)<=1:
        d=6371*acos(r)
    else :
        #print("r = ",r)
        d=0
    return(d)

def cree_contour(latmin,latmax,longmin,longmax,lat,long,n): # discretise le contour sous forme d une matrice de 0 et 1 (fonction plus ou moins inutile)
    C=np.array([np.array([0]*n)]*n)
    N=len(lat)
    paslong=(longmax-longmin)/n
    paslat=(latmax-latmin)/n
    for i in range(N):
        x=int((long[i]-longmin)/paslong)
        y=int((latmax-lat[i])/paslat)
        if x<n and y<n:
            C[y][x]=1
    return(C)


def indices_contour(latmin,latmax,longmin,longmax,lat,long,n): # renvoie les listes des indices des points du contour discrétisé
    latitude=[]
    longitude=[]
    N=len(lat)
    paslong=(longmax-longmin)/n
    paslat=(latmax-latmin)/n
    for i in range(N):
        x=int((long[i]-longmin)/paslong)
        y=int((latmax-lat[i])/paslat)
        if x<n and y<n:
            longitude.append(y)
            latitude.append(x)
    return (latitude,longitude)

def lat_long_from_indices(i,j,latmin,latmax,longmin,longmax,n): # donne les latitude et longitude à partir des indices
    paslong=(longmax-longmin)/n
    paslat=(latmax-latmin)/n
    lat=latmax-(i+0.5)*paslat
    long=longmin+(j+0.5)*paslong
    return(lat,long)

def distance_cotes(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n): # calcule la distance d'un point (indices i,j) aux cotes
    N=len(indices_lat)
    x=0
    latpoint,longpoint=lat_long_from_indices(i,j,latmin,latmax,longmin,longmax,n)
    latcote,longcote=lat_long_from_indices(indices_lat[0],indices_long[0],latmin,latmax,longmin,longmax,n)
    d=distance(latpoint,longpoint,latcote,longcote)
    for k in range(1,N):
        latcote,longcote=lat_long_from_indices(indices_lat[k],indices_long[k],latmin,latmax,longmin,longmax,n)
        d2=distance(latpoint,longpoint,latcote,longcote)
        if d2<d:
            d=d2
            x=k
    return(d,indices_lat[k],indices_long[k])       


def gradient(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n): # calcule le gradient approche d un point donné par les indices i,j
    grad_i=(distance_cotes(i+1,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)[0]-distance_cotes(i-1,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)[0])/2
    grad_j=(distance_cotes(i,j+1,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)[0]-distance_cotes(i,j-1,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)[0])/2
    return(grad_i,grad_j)

def interpolation_bilineaire(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n): #donne une approximation du gradient par une interpolation
    if float(i)==float(int(i)) and float(j)==float(int(j)) :
        gi,gj=gradient(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
    else :
        y2=int(i)
        x1=int(j)
        x2=x1+1
        y1=y2+1
        dx=j-y1
        dy=i-y1
        deltax=x2-x1
        deltay=y2-y1

        fx1y1_i,fx1y1_j=gradient(y1,x1,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
        fx1y2_i,fx1y2_j=gradient(y2,x1,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
        fx2y1_i,fx2y1_j=gradient(y1,x2,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
        fx2y2_i,fx2y2_j=gradient(y2,x2,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)

        #calcul de gi:
        deltafx=fx2y1_i-fx1y1_i
        deltafy=fx1y2_i-fx1y1_i
        deltafxy=fx1y1_i+fx2y2_i-fx2y1_i-fx1y2_i
        gi=deltafx*(dx/deltax)+deltafy*(dy/deltay)+deltafxy*((dx/deltax)*(dy/deltay))+fx1y1_i

        #calcul de gj:
        deltafx=fx2y1_j-fx1y1_j
        deltafy=fx1y2_j-fx1y1_j
        deltafxy=fx1y1_j+fx2y2_j-fx2y1_j-fx1y2_j
        gj=deltafx*(dx/deltax)+deltafy*(dy/deltay)+deltafxy*((dx/deltax)*(dy/deltay))+fx1y1_j
        """
        print("x1=",x1,"y1=",y1," -> ",fx1y1_i,fx1y1_j)
        print("x2=",x2,"y1=",y1," -> ",fx2y1_i,fx2y1_j)
        print("x2=",x2,"y2=",y2," -> ",fx2y2_i,fx2y2_j)
        print("x1=",x1,"y2=",y2," -> ",fx1y2_i,fx1y2_j)
        print("----------")
        print("x=",j,"y=",i," -> ",gi,gj)
        """
    return(gi,gj)

def matrice_avec_le_point(i,j,n): #cette fonction donne une matrice nulle partout sauf au point (i,j)
    B=np.zeros((n,n))
    B[int(i),int(j)]=5
    return(B)

def nemo_gradient(n,i,j,pas_deplac): #calcule le point nemo a l'aide de la méthode du gradient / n : le pas de la discretisation / i,j : indices du point de depart / k : pas du deplacement du point
    latmin,latmax,longmin,longmax,lat,long=getlist()
    i=(i*n)//2
    j=(j*n)//2
    indices_lat,indices_long=indices_contour(latmin,latmax,longmin,longmax,lat,long,n)
    C=cree_contour(latmin,latmax,longmin,longmax,lat,long,n)
    fig=plt.figure()
    ims=[[plt.imshow(C,animated=True)]]
    liste=[]
    for k in range(250):
        gi,gj=interpolation_bilineaire(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
        liste.append((gi,gj))
        #print("k=",k,"gi=",gi,"gj=",gj)
        if (i+(gi/pas_deplac))<n and (i+(gi/pas_deplac))>0 : i+=(gi/pas_deplac)
        if (j+(gj/pas_deplac))<n and (j+(gj/pas_deplac))>0 : j+=(gj/pas_deplac)        
        ims.append([plt.imshow(C+matrice_avec_le_point(i,j,n),animated=True)])

    ani=animation.ArtistAnimation(fig,ims,interval=150,blit=True,repeat_delay=5)

    plt.show()
    return(liste)

def matrice_des_gradients(n):
    latmin,latmax,longmin,longmax,lat,long=getlist()
    indices_lat,indices_long=indices_contour(latmin,latmax,longmin,longmax,lat,long,n)
    C=cree_contour(latmin,latmax,longmin,longmax,lat,long,n)
    G = np.zeros((n,n))
    for i in range (n):
        for j in range(n):
            gi,gj=gradient(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
            G[i][j] = gi**2 + gj**2
            #G[i][j]=distance_cotes(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)[0]
    plt.imshow(G)
    plt.show()
    return(G)


"""
def nemo_gradient2(n,i,j,pas_deplac):
    latmin,latmax,longmin,longmax,lat,long=getlist()
    i=(i*n)//2
    j=(j*n)//2
    indices_lat,indices_long=indices_contour(latmin,latmax,longmin,longmax,lat,long,n)
    gi,gj=interpolation_bilineaire(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
    while True:
        if (i+gi/pas_deplac)<n and (i+gi/pas_deplac)>0 : i+=gi/pas_deplac
        if (j+gj/pas_deplac)<n and (j+gj/pas_deplac)>0 : j+=gj/pas_deplac
        gi,gj=interpolation_bilineaire(i,j,indices_lat,indices_long,latmin,latmax,longmin,longmax,n)
        
"""
