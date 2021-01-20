import pandas as pd
import numpy as np
from tqdm import tqdm
import control_structure as cs

def create_new_testcase(number,check_digit,Qr,Qs,table,race_set,Qr_unique,Qs_unique):
    r_last_index=len(Qr_unique)+1 #それぞれの新しいインデックスを付与するための変数→初期化
    s_last_index=len(Qs_unique)+1 #+1で新しいindexをそのまま付与
    for number in range(0,len(table)):
        print(".",end='')
        Qs.append(pd.DataFrame({}))
        Qr.append(pd.DataFrame({}))
        Qs[number+1]=Qs[0].copy()
        Qr[number+1]=Qr[0].copy()
        columns=list(table.columns)
        for key in range(0,len(columns)): # 列方向のループr1→r3
            if table.iloc[number][columns[key]]>0: #race_set の交換

                #Q[i+1]のテーブルを修正
                change_event=Qr[number+1][Qr[number+1]['ID']==columns[key]].iloc[0].ID # receiveの交換するやつr3
                change_event_number=Qr[number+1][Qr[number+1]['ID']==columns[key]].iloc[0].name #r3の行番号→2
                try:
                    new_partner=race_set[Qr[number+1][Qr[number+1]['ID']==columns[key]].iloc[0].ID][int(table.iloc[number][columns[key]])-1] #sendの新しいパートナー s4
                    new_partner_number=Qs[number+1][Qs[number+1]['ID']==new_partner].iloc[0].name #s4の行番号→3
                except:
                    continue


                ## QSのindexを振りなおす処理
                new_index=[]
                for j in range(0,len(Qr[number+1])):
                    if j==change_event_number:
                        new_index.append(new_partner_number)
                    elif j==new_partner_number:
                        new_index.append(change_event_number)
                    else:
                        new_index.append(j)

                Qs[number+1]['new_index']=new_index
                Qs[number+1]=Qs[number+1].set_index('new_index')
                Qs[number+1].sort_index(inplace=True)


                #==========Qrの重複追加作業=================

        for index,row in Qr[number+1].iterrows():
            results=cs.cstruct(Qr,Qs,Qr[number+1].iloc[index],[],check_digit,number,Qs_unique)
            judge=False
            if results: #空だったらnot 
                for index2,row2 in Qr_unique.iterrows():
                    if results==Qr_unique.at[index2,'cstruct']:
                        new_index=index2
                        judge=True
                        break
                if not judge: #Falseだったら判定
                    Qr[number+1].at[index,'ID']='r'+str(r_last_index)
                    #Qr[number+1].at[index,'cstruct']=results
                    r_last_index+=1
                    temp=list(Qr[number+1].iloc[index])
                    temp=temp[:5]
                    temp.append(results)
                    temp=pd.Series(temp,index=Qr_unique.columns,name=len(Qr_unique))
                    #temp=pd.DataFrame(,columns=Qr_unique.columns)
                    #Qr_unique.append(temp,ignore_index=False)
                    #pd.concat([Qr_unique,temp],axis=0)
                    Qr_unique.loc[len(Qr_unique)]=temp
                else:
                    Qr[number+1].iloc[index]=Qr_unique.iloc[new_index]
            else:
                pass


    return {'recv':Qr,'send':Qs}