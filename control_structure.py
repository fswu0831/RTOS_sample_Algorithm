import pandas as pd

def cstruct(Qr,Qs,event,results,check_digit,number,Qs_unique):
    
    if check_digit==0:
        magic=0
    else:
        magic=1
    
    thread=event['Thread']
    index=event['Index']
       
    if index==1:
        return ''
    for i in range(index-1,0,-1):
        try:
            temp=Qr[number+magic][(Qr[number+magic].Thread == thread) & (Qr[number+magic].Index==i)].iloc[0]
        except:
            temp=Qs[number+magic][(Qs[number+magic].Thread == thread) & (Qs[number+magic].Index==i)].iloc[0]
        if temp['Event']=='send':
            results.append(temp['ID'])
            send=temp
            results.extend(Qs_unique[Qs_unique.ID==send.ID].iloc[0].cstruct)
        else:
            results.append(temp['ID'])
            send=Qs[number+magic].iloc[temp.name]
            results.append(send['ID'])
            results.extend(Qs_unique[Qs_unique.ID==send.ID].iloc[0].cstruct)
    return list(set(results))

def cstruct_init(Qr,Qs,event,s_list):    
    results=[]
    thread=event['Thread']
    index=event['Index']
       
    if index==1:
        return ''
    for i in range(index-1,0,-1):
        try:
            temp=Qr[0][(Qr[0].Thread == thread) & (Qr[0].Index==i)].iloc[0]
        except:
            temp=Qs[0][(Qs[0].Thread == thread) & (Qs[0].Index==i)].iloc[0]
        if temp['Event']=='send':
            results.append(temp['ID'])
            send=temp
            if len(s_list)>send.name: 
                results.extend(s_list[send.name])
        else:
            results.append(temp['ID'])
            send=Qs[0].iloc[temp.name]
            results.append(send['ID'])
            if len(s_list)>send.name: 
                results.extend(s_list[send.name])
    return list(set(results))