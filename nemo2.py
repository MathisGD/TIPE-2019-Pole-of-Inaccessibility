import numpy as np
import xlrd
from math import *
import matplotlib.pyplot as plt

def getlist(): # donne les lat et long sous forme d'une liste (les angles sont convertis en radians)
    document = xlrd.open_workbook("D:\TIPE\donnees cotes\golfe_du_mex.xls")

    print("Nombre de feuilles: "+str(document.nsheets))
    print("Noms des feuilles: "+str(document.sheet_names()))
    feuille_1 = document.sheet_by_index(0)
    feuille_1 = document.sheet_by_name("Feuille1")
    print("Format de la feuille 1:")
    print("Nom: "+str(feuille_1.name))
    print("Nombre de lignes: "+str(feuille_1.nrows))
    print("Nombre de colonnes: "+str(feuille_1.ncols))
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
    d=6371*acos(cos(lat1)*cos(lat2)*cos(long1-long2)+sin(lat1)*sin(lat2))
    return(d)

def nemo_naif(latmin,latmax,longmin,longmax,lat,long,n): # effectue le calcul naif du point nemo
    paslong=(longmax-longmin)/n
    paslat=(latmax-latmin)/n
    dinit=distance(latmin,longmin,latmax,longmax)
    dist=np.array([np.array([dinit]*n)]*n)
    N=len(lat)
    for k in range(N):
        for i in range(n):
            for j in range(n):
                d=distance(lat[k],long[k],latmax-(paslat/2)-i*paslat,longmin+(paslong/2)+j*paslong)
                if d<dist[i][j]:
                    dist[i][j]=d
    dnem=np.max(dist)
    I,J=np.where(dist==dnem)
    latnem=latmax-(paslat/2)-I[0]*paslat
    longnem=longmin+(paslong/2)+J[0]*paslong
    print(dist[I[0]][J[0]])
    return(degrees(latnem),degrees(longnem))
    
    
    













    
