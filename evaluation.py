import pandas as pd
import numpy as np
from tqdm import tqdm

def evaluate(Qr,Qs,race_set):
    print('Evaluating')
    Q=pd.concat([Qs[0],Qr[0]]).sort_index()
    V=Qr[0].Port.unique()
    T=np.sort(Q.Thread.unique())
    V_total_number=len(V)
    T_total_number=len(T)
    race_num=RACE(race_set)
    svqr=SVQR(Qr,Qs)
    def_use=Def_Use(Qr,Qs)
    plnv=Plnv(Qr,Qs)
    return {'SYN':len(Qr[0]),'Task':T_total_number,'TestCase':len(Qr),'Buffer':V_total_number,'SVAR':div(svqr),'Def-Use':div(def_use),'Plnv':div(plnv),'Race':race_num}

def factorial(n):
    sum=1
    for i in range(1,n+1):
        sum*=i
    return sum

def combination(n,k):
    return int(factorial(n)/(factorial(n-k)*factorial(k)))

def RACE(race_set):
    sum=0
    for key in race_set.keys():
        sum+=len(race_set[key])
    return sum

def SVQR(Qr,Qs):
    #総数の計算
    Q=pd.concat([Qs[0],Qr[0]]).sort_index()
    V=Qr[0].Port.unique()
    T=Q.Thread.unique()
    V_total_number=len(V)
    T_total_number=len(T)

    total_number=0

    for l in range(V_total_number):
        for i in range(0,T_total_number-1):
            for j in range(i+1,T_total_number):
                k=len(Q[(Q.Thread==T[i]) &(Q.Port==V[l])])
                n=k+len(Q[(Q.Thread==T[j]) &(Q.Port==V[l])])
                total_number+=combination(n,k)

    #数値計算
    value=0
    for l in range(V_total_number):
        for i in range(0,T_total_number-1):
            for j in range(i+1,T_total_number):
                log=pd.DataFrame({})
                for loop in range(len(Qr)):
                    Q=pd.concat([Qs[loop],Qr[loop]]).sort_index()

                    array=Q[((Q.Thread==T[i]) & (Q.Port==V[l])) | ((Q.Thread==T[j]) &(Q.Port==V[l]))].Thread
                    array=array.reset_index()
                    
                    log=log.append(array.Thread,ignore_index=True)
                
                try:
                    log=log[~log.duplicated()]
                except:
                    pass
            
                value+=len(log)
    return {'total_number':total_number,'number':value}

def Def_Use(Qr,Qs):
    Q=pd.concat([Qs[0],Qr[0]]).sort_index()
    V=Qr[0].Port.unique()
    T=np.sort(Q.Thread.unique())
    V_total_number=len(V)
    T_total_number=len(T)
    
    total_number=len(Qr[0]) #Nr
    
    for l in range(V_total_number):
        for i in range(0,T_total_number-1):
            for j in range(i+1,T_total_number):
                Nr=len(Qr[0][(Qr[0].Thread==T[i]) & (Qr[0].Port==V[l])])
                Ns=len(Qs[0][(Qs[0].Thread==T[j]) & (Qs[0].Port==V[l])])
                sum=(Nr*Ns)
                total_number+=sum
                
                Nr=len(Qr[0][(Qr[0].Thread==T[j]) & (Qr[0].Port==V[l])])
                Ns=len(Qs[0][(Qs[0].Thread==T[i]) & (Qs[0].Port==V[l])])
                sum=(Nr*Ns)
                total_number+=sum
                
    value=0
    for l in range(V_total_number):
        for i in range(0,T_total_number):

                for recv in range(2):
                    log=pd.DataFrame({})
                    for loop in range(len(Qr)):     
                        array=pd.Series([],name=len(log))
                        Qr_event=Qr[loop][(Qr[loop].Thread==T[i]) & (Qr[loop].Port==V[l])]
                        Qr[loop]['KEY']=Qr[loop]['Thread']+'-'+Qr[loop]['Index'].astype(str)
                        Qs[loop]['KEY']=Qs[loop]['Thread']+'-'+Qs[loop]['Index'].astype(str)
                        for k in range(len(Qr_event)):
                            array[k]=Qs[loop].iloc[Qr_event.iloc[k].name].KEY
                        if array.any():
                            log=log.append(array,ignore_index=True)
                        else:
                            pass
                    log=log[~log.duplicated()]
                    value+=len(log)
    return {'total_number':total_number,'number':value}

def Plnv(Qr,Qs):
    Q=[]
    
    for i in range(len(Qr)):
        Q.append(pd.DataFrame({})) #新しいテーブルを作成
        Q[i]=pd.concat([Qs[i],Qr[i]]).sort_index()
        Q[i]=Q[i].reset_index(drop=True)
    V=Qr[0].Port.unique()
    T=Q[0].Thread.unique()
    V_total_number=len(V)
    T_total_number=len(T)

    total_number=0

    for l in range(V_total_number):
        for i in range(0,T_total_number):
            PNi=len(Q[0][(Q[0].Thread==T[i]) & (Q[0].Port==V[l])])-1
            if PNi<=0:
                continue
            else:
                Nj=len(Q[0][(Q[0].Thread!=T[i]) & (Q[0].Port==V[l])])
                total_number+=PNi*Nj+PNi

    value=0
    
    for l in range(V_total_number):
        for i in range(0,T_total_number):
            df=Q[0][(Q[0].Thread==T[i]) & (Q[0].Port==V[l])]
            
            if len(df)<=1:
                continue
            else:
                for j in range(len(df)-1):
                    array=[]
                    for loop in range(len(Qr)):
                        Qr[loop]['KEY']=Qr[loop]['Thread']+'-'+Qr[loop]['Index'].astype(str)
                        Qs[loop]['KEY']=Qs[loop]['Thread']+'-'+Qs[loop]['Index'].astype(str)
                        df=Q[loop][(Q[loop].Thread==T[i]) & (Q[loop].Port==V[l])]
                        
                        temp=Q[loop][df.iloc[j].name+1:df.iloc[j+1].name]
                        temp=temp[temp.Port==V[l]]
                        if len(temp)==0:

                            array.append(0)
                        for k in range(len(temp)):
                            array.append(temp.iloc[k].KEY)
                        array=list(set(array))
                    value+=len(array)
    return {'total_number':total_number,'number':value}

def div(dic):
    return dic['number']/dic['total_number']

