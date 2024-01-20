import streamlit as st
import pandas as pd
import streamlit_nested_layout
from st_mui_dialog import st_mui_dialog
import datetime
from zoneinfo import ZoneInfo
import time
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from PIL import Image

def show_cancel():
    name = st.selectbox(
            'Input your name',
            ('Nishio', 'Wang.S', 'Rashid', 'Wang.J', 'Saida', 'Katabira', 'Nakamizo', 'Matono',
             'Okuda', 'Taki', 'Sato', 'Watanabe'),
            index=None, placeholder="Select your name")
    # 名前が選択されていない場合は、warningを出す
    if name == None:
        st.warning("Please select your name.")
        return
    # pc_reserves.csvの読み込み
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"]).dt.tz_localize('Asia/Tokyo')
    df_reserve["End"] = pd.to_datetime(df_reserve["End"]).dt.tz_localize('Asia/Tokyo')
    dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    # 予約終了日時が現在日時よりも前の予約情報を削除
    df_reserve = df_reserve[df_reserve["End"] >= dt_now]
    # その予約者の予約情報のみに絞り込み
    df_reserve = df_reserve[df_reserve["User"] == name]
    # 予約情報がない場合は、warningを出す
    if len(df_reserve) == 0:
        st.warning("You have no reservations.")
        return
    st.markdown('## Reservations')
    df_reserve = df_reserve.reset_index(drop=True)
    for i in range(len(df_reserve)):
        row = df_reserve.loc[i]
        pc_name = row["PC"]
        date_start = row["Start"]
        date_end = row["End"]
        with st.expander('### Reservation ' + str(i + 1), expanded=True):
            st.markdown('PC: ' + pc_name)
            st.markdown('Start: ' + str(date_start)[:-9])
            st.markdown('End: ' + str(date_end)[:-9])
            # is_click = st.dialog("Clear with close", close_on_submit=False, clear_on_close=True)#st.button("Cancel", key=i)
            is_click = st_mui_dialog("Cancel Reservation", "Are you sure to cancel this reservation?", key=i, button_txt="Cancel Reservation")
            if is_click:
                cancel(row)
        
def cancel(row):
    """予約をキャンセル
    Args:
        row (Series): 予約情報
    """
    row = row.drop("Unnamed: 0")
    with st.spinner('Canceling...'):
        time.sleep(2)
    # 予約情報をpc_reserves.csvから削除
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"]).dt.tz_localize('Asia/Tokyo')
    df_reserve["End"] = pd.to_datetime(df_reserve["End"]).dt.tz_localize('Asia/Tokyo')
    # rowとPC、User、Start、Endが一致する行を削除
    df_reserve = df_reserve[~((df_reserve["PC"] == row["PC"]) & (df_reserve["User"] == row["User"]) & (df_reserve["Start"] == row["Start"]) & (df_reserve["End"] == row["End"]))]
    df_reserve = df_reserve.reset_index(drop=True)
    df_reserve = df_reserve.drop("Unnamed: 0", axis=1)
    df_reserve["Start"] = df_reserve["Start"].dt.tz_localize(None)
    df_reserve["End"] = df_reserve["End"].dt.tz_localize(None)
    df_reserve.to_csv("pc_reserves.csv")
    st.success("Successfully Canceled.")

def login():
    """ログイン処理
    一応、ログイン処理をする（必須ではないと思うが、一応）
    パスワードも一応、ハッシュ化したものを使う
    Returns:
        _type_: _description_
    """
    with open('config.yml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # config
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    
    name, authentication_status, username = authenticator.login('Login', 'main')
    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    return authentication_status, username
                
if __name__ == "__main__":
    img_icon = Image.open("icon.jpg")
    st.set_page_config(
        page_title="PC Reserve App",
        page_icon=img_icon
    )
    st.title("PC Reservation System")
    is_logined, username = login()
    if is_logined:
        st.header("Cancel Reservation")
        show_cancel()
