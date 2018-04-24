# -*- coding: utf-8 -*-
#Programmato da Davide Leone in Python 3 - Per contatti: leonedavide[at]protonmail.com
#Versione 0.6.2 del 24/04/2018
#Distribuito sotto licenza GNU Lesser General Public License - Copyright 2018 Davide Leone
""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

#Dizionari e costanti
simboli_mate = ['+','(',')','-','*','/','^',"!",":"]
simboli = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
numeri_arabi = ['0','1','2','3','4','5','6','7','8','9']
alfabeto_min = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alfabeto_mai = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
pi = 3.141592653589793
eulero = 2.718281828459045
aureo = 1.618033988749895
gelford = 23.14069263277927
c =  299792458
markdown = ['[',']','(',')','*','_','`']

#Funzioni

def apri(file,fin="r"): #Apre un file in formato lettura (eviitando gli errori)
    try:
        open(file,'r')
    except:
        open(file,'w')
    finally:
        val = open(file,fin)
        return val

def carica(filename,dati): #Carica un valore in un file binario
    import pickle
    file = apri(filename,'wb')
    pickle.dump(dati,file)
    file.close()
    
def cataloga(file,chiave,valore):
    #Dato un dizionario JSON-like, ed una chiave, restituisce tutti gli oggetti che hanno un certo valore corrispodente
    catalogo = []
    if type(file) is dict:
        chiavi = list(file.keys())
        for x in range(len(chiavi)):
            indice = chiavi[x]
            try:    
                if file[indice][chiave] == valore:
                    catalogo.append(indice)
            except:
                None
    else:
        None
    return catalogo

def delistizza(testo): #Trasformare una lista in stringa
    stringa = ''
    for x in range(len(testo)):
        stringa += testo[x]
    return stringa

def elimina(testo,indice): #Elimina una parte del testo
    try:
        indice =int(indice)
        n = len(testo)
    except:
        raise
    else:
        if indice < 0:
            return estrai(testo,n+indice)
        elif indice > 0:
            return estrai(testo,indice-n)
        else:
            return

def elimina_carattere(testo,carattere): #Elimina un carattere da un testo
    nuovo_testo = ''
    for x in range(len(testo)):
        if testo[x] != carattere:
            nuovo_testo += testo[x]
    return nuovo_testo

def elimina_caratteri(testo,lista):
    for x in range(len(lista)):
        testo = elimina_carattere(testo,lista[x])
    return testo

def elimina_estremi(testo,indice): #Elimina gli estremi di un testo
    testo = elimina(testo,indice)
    testo = elimina(testo,-indice)
    return testo

def elimina_posizione(testo,indice): #Elimina una posizione da un testo
    return sostituisci_posizione(testo,'',indice)

def esclusioni(testo,lista): #Controlla se i valori di una lista sono presenti nel testo
    testo = str(testo)
    for x in range(len(lista)):
        if lista[x] in testo:
            return True
    return False

def estrai(testo,numero): #Recupera una parte del testo
    est = ''
    c = 1
    try:
        numero = int(numero)
        if abs(numero) > len(testo):
            return testo
        if numero < 0:
            numero = numero*-1
            for x in range(numero):
                x  += 1
                est += str(testo)[x*-1] #Prende a partire della fine
            est = est[::-1] #Inverte il testo
        else:
            for x in range(numero):
                est += str(testo)[x]
        return est
    except:
        raise

def fattoriale(n): #Fattoriale di n
    if n == 0: 
        return 1 
    else: 
        fat = fattoriale(n-1) 
        risultato = n*fat 
        return risultato

def index(testo,carattere):
    indice = []
    for x in range(len(testo)):
        if testo[x] == carattere:
            indice.append(x)
    return indice

def ordina(lista):
    nlista = []
    for x in range(len(lista)):
        nlista.append(min(lista))
        lista.remove(min(lista))
    return nlista

def pari(numero):
    numero = int(numero)
    if numero % 2 == 0:
        return True
    else:
        return False
    
def parole(text,delta=' '): #Divide un testo in parole
    text = str(text)
    x = 0
    t = ''
    parole = []
    while 1:
        try:
            c = text[x]
        except IndexError:
            if t != '':
                parole.append(t)
            break
        x += 1
        if c == delta:
            if t != '':
                parole.append(t)
            t = ''
        else:
            t += c
    return parole

def scarica(filename,eccezione=None): #Scarica il valore di un file binario
    import pickle
    try:
        file = open(filename,'rb')
        dati = pickle.load(file)
        file.close()
        return dati
    except:
        if eccezione == None:
            raise
        else:
            return eccezione

def scrivi(filename,dati,mod='a'): #Scrive un valore all'interno di un file
    file = open(filename,mod)
    file.write(dati)
    file.close()

def sostituisci(testo,le1,le2): #Sostituisce un carattere con un altro
    parola = ''
    for x in range(len(testo)):
        c = testo[x]
        if c == le1:
            c = le2
        parola += c
    return parola

def sostituisci_posizione(testo,carattere,posizione):
    testo = list(testo)
    testo[posizione] = carattere
    return delistizza(testo)

def superparole(testo,lista):
    #Divide un testo in parole, usando come discriminante tutti i valori del dizionario
    text = str(text)
    x = 0
    t = ''
    parole = []
    while 1:
        try:
            c = text[x]
        except IndexError:
            if t != '':
                parole.append(t)
            break
        x += 1
        if esclusioni(c,lista) == True:
            if t != '':
                parole.append(t)
            t = ''
        else:
            t += c

    return parole
