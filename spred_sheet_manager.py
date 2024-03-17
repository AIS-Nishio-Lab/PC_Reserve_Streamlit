"""
おそらくかなり冗長に書いてあるように見えるだろうが、スプレッドシートは普通の型以外を突っ込むと、うまく動作しないことがあるので、(int, float, str)あたりの型のみで対処する
"""
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def read_spreadsheet(is_use_cache=True):
    if not is_use_cache:
        st.cache_data.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    df = df.dropna(how="all").dropna(how='all', axis=1)
    lists = []
    for i in range(df.shape[0]):
        _list = []
        _list.append(int(df.iloc[i,0]))
        _list.append(str(df.iloc[i,1]))
        _list.append(str(df.iloc[i,2]))
        # column 3-7 is start time
        _start_time = pd.Timestamp(int(df.iloc[i,3]), int(df.iloc[i,4]), int(df.iloc[i,5]), int(df.iloc[i,6]), int(df.iloc[i,7]))
        _list.append(_start_time)
        # column 8-12 is end time
        _end_time = pd.Timestamp(int(df.iloc[i,8]), int(df.iloc[i,9]), int(df.iloc[i,10]), int(df.iloc[i,11]), int(df.iloc[i,12]))
        _list.append(_end_time)
        lists.append(_list)
    df = pd.DataFrame(lists, columns=["Unnamed: 0", "PC", "User", "Start", "End"])
    df.to_csv("pc_reserves.csv", index=False)
    return df

def update_spreadsheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = pd.read_csv("pc_reserves.csv")
    df.iloc[:,3] = pd.to_datetime(df.iloc[:,3])
    df.iloc[:,4] = pd.to_datetime(df.iloc[:,4])
    save_list = [["Unnamed: 0", "PC", "User", "Start Year", "Start Month", "Start Day", "Start Hour", "Start Minute", "End Year", "End Month", "End Day", "End Hour", "End Minute"]]
    for i in range(df.shape[0]):
        _list = []
        _list.append(int(df.iloc[i,0]))
        _list.append(str(df.iloc[i,1]))
        _list.append(str(df.iloc[i,2]))
        _list.append(df.iloc[i,3].year)
        _list.append(df.iloc[i,3].month)
        _list.append(df.iloc[i,3].day)
        _list.append(df.iloc[i,3].hour)
        _list.append(df.iloc[i,3].minute)
        _list.append(df.iloc[i,4].year)
        _list.append(df.iloc[i,4].month)
        _list.append(df.iloc[i,4].day)
        _list.append(df.iloc[i,4].hour)
        _list.append(df.iloc[i,4].minute)
        save_list.append(_list)
    df = pd.DataFrame(save_list[1:], columns=save_list[0])
    conn.update(data=df)
    st.cache_data.clear()
