import pandas as pd
import control_structure as cs

def delete_diff(Qr,Qs):
    if len(Qr[0])>len(Qs[0]):
        Qr[0]=Qr[0][:len(Qs[0])]
    elif len(Qr[0])<len(Qs[0]):
        Qs[0]=Qs[0][:len(Qr[0])]
    return
    
def init(table):
    table['Thread']=table['Thread'].map(lambda x:'T'+str(x))
    r_list=list(range(1,len(table)+1))
    r_list=list(map(lambda x:'r'+str(x),r_list)) #['r1', 'r2', 'r3', 'r4']
    table.insert(0,'ID',r_list) #attach the name of event
    return table

def append_unique(Qr,Qs):
    r_list=[]
    s_list=[]
    for i in range(0,len(Qr[0])):
        r_list.append(cs.cstruct(Qr,Qs,Qr[0].iloc[i],[],0,0))
        s_list.append(cs.cstruct(Qr,Qs,Qs[0].iloc[i],[],0,0))
    Qr_unique=Qr[0].copy()
    Qs_unique=Qs[0].copy()
    Qr_unique.insert(len(Qr_unique.columns),'cstruct',r_list)
    Qs_unique.insert(len(Qs_unique.columns),'cstruct',s_list)
    
    return {'Qr':Qr_unique,'Qs':Qs_unique}