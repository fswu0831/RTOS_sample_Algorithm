import pandas as pd
import control_structure as cs
import numpy as np
from tqdm import tqdm

def init_main(Qr,Qs):
    delete_diff(Qr,Qs)
    Qr=arrange_data(Qr,Qs)
    Qr[0]=init(Qr[0],'r')
    Qs[0]=init(Qs[0],'s')
    df_unique=append_unique(Qr,Qs)
    Qr_unique=df_unique['Qr']
    Qs_unique=df_unique['Qs']
    print('finish initialize')
    return {'Qr':Qr,'Qs':Qs,'Qr_unique':Qr_unique,'Qs_unique':Qs_unique}


def delete_diff(Qr,Qs):
    if len(Qr[0])>len(Qs[0]):
        Qr[0]=Qr[0][:len(Qs[0])]
    elif len(Qr[0])<len(Qs[0]):
        Qs[0]=Qs[0][:len(Qr[0])]
    return
    
def init(table,string):
    table['Thread']=table['Thread'].map(lambda x:'T'+str(x))
    r_list=list(range(1,len(table)+1))
    r_list=list(map(lambda x:string+str(x),r_list)) #['r1', 'r2', 'r3', 'r4']
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

def arrange_data(Qr,Qs):
    for i in range(len(Qs[0])):
        if Qr[0].iloc[i].Port==Qs[0].iloc[i].Port:
            pass
        else: #一致しなかった場合
            port=Qs[0].iloc[i].Port
            df=Qr[0][i+1:]
            if len(df)==0:
                continue
            else:
                new_index=np.arange(len(Qr[0]))
                new_pair_index=df[df.Port==port].iloc[0].name
                new_index[i]=new_pair_index
                new_index[new_pair_index]=i
                Qr[0]['new_index']=new_index
                Qr[0]=Qr[0].set_index('new_index')
                Qr[0].sort_index(inplace=True)
    return Qr