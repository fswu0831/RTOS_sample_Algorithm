import pandas as pd
from allpairspy import AllPairs
from collections import OrderedDict
import time
import numpy as np
import control_structure as cs
from tqdm import tqdm

def no_index(Qr,Qs,start,finish,t,event,R):
    #if type(event)==int:
    #    event=Qr[(Qr.ID==R[finish])].iloc[0]
    for l in range(start,finish):
        if t[l]>0 and R[l] in cs.cstruct(Qr,Qs,event,[],0,0):
            return True
        else:
            continue
    return False

def construct_race_table(Qs,Qr,race_set,t_way):
    R=[] #create race_set
    D=[] #number of race_set
    heading=[] #{r1,r2,....r}

    R.append('')
    D.append('')
    heading.append('dummy')
    count=0
    for key in race_set.keys():
        if len(race_set[key])>0:
            R.append(key) # raceのあるイベントを追加
            D.append(len(race_set[key])) #raceの数を追加
            heading.append(key) # r
            count=count+1
            if count>=t_way and t_way>1:
                break
    table=pd.DataFrame([],columns=heading)

    t=np.zeros(len(R)) #raceの数分の配列 #t[0]はダミー

    while True:
        print(".",end='')
        results=[]

        max_index=''
        for i in range(len(t)-1,0,-1):
            if t[i]<D[i] and t[i]!=-1:
                max_index=i
                break
        if max_index=='':
            break
        t[i]+=1

        if t[i]==1: #just changed t[i] from 0 to 1

            for j in range(i+1,len(R)):
                if t[j]!=-1 and (Qr[0][Qr[0].ID==R[i]].iloc[0].ID in cs.cstruct(Qr,Qs,Qr[0][Qr[0].ID==R[j]].iloc[0],[],0,0)):

                    t[j]=-1

        for j in range(i+1,len(R)):
            if(t[j]==D[j]):
                t[j]=0 #just change t[j] from dj to 0

                for k in range(j+1,len(R)):
                    if t[k]==-1 and Qr[0][Qr[0].ID==R[j]].iloc[0].ID in cs.cstruct(Qr,Qs,Qr[0][Qr[0].ID==R[k]].iloc[0],[],0,0) and no_index(Qr,Qs,1,k,t,Qr[0][(Qr[0].ID==R[k])].iloc[0],R):
                        t[k]=0
        #let s be the t[i] sending event in race_set(ri)
        s= race_set[R[i]][int(t[i])-1] 


        if no_index(Qr,Qs,1,len(R)-1,t,Qs[0][(Qs[0].ID==s)].iloc[0],R)==False:
            table=table.append(pd.Series(t,index=table.columns),ignore_index=True)
    return table.drop('dummy',axis=1)

def expand_table(Qr,Qs,race_set,table,t_way):
    print('Expanding table')
    for way in range(t_way,len(Qr[0])): #1列ずつ足していくためのループ
        print(".",end='')
        new_event=Qr[0].iloc[way]

        if (len(race_set[Qr[0].iloc[way].ID]))>0: #raceがあるかどうか確認

            ## 横方向の拡張

            pi=[]
            heading=table.columns
            for i in range(len(heading)):
                pi.append(pd.DataFrame({heading[i]:[],new_event.ID:[]}))
                heading2=pi[i].columns
                for j in range(len(heading2)):              
                    new_row=pd.Series([])
                    parameters_dict={}
                    heading=table.columns.values
                    for i2 in range(len(heading)):
                        parameters_dict[heading[i2]]=[]
                        for j2 in range(len(race_set[heading[i2]])+1):
                            parameters_dict[heading[i2]].append(j2)
                    parameters=OrderedDict(parameters_dict)
                    for k, pairs in enumerate(AllPairs(parameters)):
                        new_row[len(new_row)]=pairs[j]
                    pi[i][heading2[j]]=new_row
                pi[i]=pi[i][pi[i].sum(axis=1)!=0]
                pi[i]=pi[i].reset_index(drop=True)

            table[new_event.ID]=''
            for index in range(len(table)):#tableのループ
                match_count_array=[]
                for race_num in range(len(race_set[Qr[0].iloc[way].ID])+1): #raceの数だけループ
                    match_count_array.append(0)
                    check_array=table.iloc[index]
                    check_array[new_event.ID]=race_num
                    for i in range(len(pi)):#piごとにループ
                        check_array_edit=check_array[pi[i].columns]
                        for j in range(len(pi[i])):
                            if (check_array_edit==pi[i].iloc[j]).all():
                                match_count_array[race_num]+=1
                max_value=max(match_count_array) #raceの中からカバーできる最大値を取得
                max_index=match_count_array.index(max_value)
                table.at[index,new_event.ID]=max_index #tableに新しいデータを追加
                    #ついかした組み合わせがあるものを削除
                delete_array=table.iloc[index]
                for i in range(len(pi)):
                    delete_array_edit=delete_array[pi[i].columns]
                    for j in range(len(pi[i])):
                        if (delete_array_edit==pi[i].loc[j]).all():
                            pi[i].drop(j,inplace=True)
                    pi[i]=pi[i].reset_index(drop=True)
            ## 縦方向の拡張
            for i in range(len(pi)):
                for j in range(len(pi[i])):
                    table=table.append(pi[i].iloc[j])# 最終行を挿入
                    table=table.reset_index(drop=True)
                    last_data=table.iloc[len(table)-1]#最終行を取得
                    #これ以降は最終行の欠損地を埋めていく処理
                    for k in range(len(last_data)):
                        if last_data.isna()[k]:#欠損地のとき
                            # 制御構造に入っているか確認
                            #一個前に値がなければnot-1
                            for l in range(k,0,-1):
                                if last_data[l-1]==1:
                                    if Qr[0][Qr[0].ID==list(table.columns)[l-1]].iloc[0].ID in cs.cstruct(Qr,Qs,Qr[0][Qr[0].ID==list(table.columns)[k]].iloc[0],[],0,0):
                                        table.at[len(table)-1,list(table.columns)[k]]=-1
                                        break
                                        #制御構造
                        ##-1は既に埋まっている
                        table=table.fillna(0)
    return table