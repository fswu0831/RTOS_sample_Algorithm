import pandas as pd

def cstruct(Qr,Qs,event,results,check_digit,number):    
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
            event=temp
            results.extend(cstruct(Qr,Qs,event,results,check_digit,number))
        else:
            results.append(temp['ID'])
            send=Qs[number+magic].iloc[temp.name]
            results.append(send['ID'])
            results.extend(cstruct(Qr,Qs,send,results,check_digit,number))
    return list(set(results))