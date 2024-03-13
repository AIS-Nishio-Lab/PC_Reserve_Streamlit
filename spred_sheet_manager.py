import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def read_spreadsheet(is_use_cache=True):
    if not is_use_cache:
        st.cache_data.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    df = df.dropna(how="all").dropna(how='all', axis=1)
    # column1 to int
    df.iloc[:,0] = df.iloc[:,0].astype(int)
    # start column to timestamp
    df.iloc[:,3] = pd.to_datetime(df.iloc[:,3])
    df.iloc[:,4] = pd.to_datetime(df.iloc[:,4])
    df.to_csv("pc_reserves.csv", index=False)
    return df

def update_spreadsheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = pd.read_csv("pc_reserves.csv")
    df.iloc[:,3] = pd.to_datetime(df.iloc[:,3])
    df.iloc[:,4] = pd.to_datetime(df.iloc[:,4])
    conn.update(data=df)
    st.cache_data.clear()
