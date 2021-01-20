import pandas as pd
import control_structure as cs

def combination_check(combination_table,port,send1,send2,recv1,recv2):
    for index in range(len(combination_table)):
        check=combination_table.iloc[index]
        if check.PORT==str(port) and send1 in str_to_list(check.SEND) and send2 in str_to_list(check.SEND) and recv1 in str_to_list(check.RECV) and recv2 in str_to_list(check.RECV):
            return False
        
    return True


def str_to_list(string):
    l=string.split(',')
    list=[]
    for i in range(len(l)):
        if i==0:
            if len(l)==1:
                list.append(l[i][1:len(l[i])-1])
            else:
                list.append(l[i][1:])
        elif i==len(l)-1:
            list.append(l[i][:len(l[i])-1])
        else:
            list.append(l[i])
    return list






def creating_race_set(Qr,Qs,Qs_unique,race_set,combination):
    combination_table=pd.DataFrame({},columns=['PORT','SEND','RECV'],dtype='object')
    # race_set の初期化
    for i in range(len(Qr[0])):

        race_set[Qr[0].iloc[i].ID]=[]

    # sでループ
    for i in range(len(Qs[0])):

        number=Qs[0].iloc[i].name
        ID=Qs[0].iloc[i].ID
        thread=Qs[0].iloc[i].Thread
        port=Qs[0].iloc[i].Port

        pair_event=Qr[0].iloc[number]

        Qr_temp=Qr[0][(Qr[0].Thread==pair_event.Thread) & (Qr[0].Port==pair_event.Port) & (Qr[0].Index<pair_event.Index)] # race_setの候補
        for j in range(len(Qr_temp)):
            s_dash=Qs[0].loc[Qr_temp.iloc[j].name]
            if s_dash.ID not in Qs_unique[Qs_unique.ID==ID].iloc[0].cstruct:
                if combination==1:
                    if combination_check(combination_table,port,thread,s_dash.Thread,pair_event.Thread,Qr_temp.iloc[j].Thread):
                        race_set[Qr_temp.iloc[j].ID].append(ID)
                        send_set='['+thread+','+s_dash.Thread+']'
                        recv_set='['+pair_event.Thread+','+Qr_temp.iloc[j].Thread+']'
                        data=[str(port),send_set,recv_set]
                        append_table=pd.DataFrame(data=[data],columns=['PORT','SEND','RECV'],dtype='object')
                        combination_table=combination_table.append(append_table,ignore_index=True)
                elif combination==0:
                    race_set[Qr_temp.iloc[j].ID].append(ID)
    return race_set

