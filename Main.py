import streamlit as st
import streamlit_authenticator as stauth
from streamlit_calendar import calendar
from st_mui_dialog import st_mui_dialog
import pandas as pd
import datetime
from zoneinfo import ZoneInfo
import yaml
from yaml.loader import SafeLoader
import time
from PIL import Image
from spred_sheet_manager import read_spreadsheet, update_spreadsheet

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

def now_using():
    """現在使用中のPCを表示
    Returns:
        _type_: _description_
    """
    st.header("Current Using PC")
    # df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve = read_spreadsheet()
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"]).dt.tz_localize('Asia/Tokyo')
    df_reserve["End"] = pd.to_datetime(df_reserve["End"]).dt.tz_localize('Asia/Tokyo')
    dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    current_using = df_reserve[(df_reserve["Start"] <= dt_now) & (dt_now <= df_reserve["End"])]
    df_pcs_name = pd.read_csv("pc_specs.csv")["PC"].values
    table_list = []
    for pc_name in df_pcs_name:
        if pc_name in current_using["PC"].values:
            using = current_using[current_using["PC"] == pc_name]
            table_list.append([pc_name, using["User"].values[0],
                               using["Start"].iloc[0].strftime("%Y/%m/%d %H:%M"),
                               using["End"].iloc[0].strftime("%Y/%m/%d %H:%M")])
        else:
            table_list.append([pc_name, "No use now", "", ""])
    df = pd.DataFrame(table_list, columns=["PC", "User", "Start", "End"])
    st.table(df)
    return

def reserve_form():
    """PCの予約フォーム
    """
    st.header("Reserve PC")
    on = st.toggle('Show Reservation Form', False)
    if not on:
        return
    name = st.selectbox(
            'Input your name',
            ('Nishio', 'Wang.S', 'Rashid', 'Wang.J', 'Yu', 'Saida', 
             'Nakamizo', 'Matono',
             'Wang.Z',
             'Sato', 
             'Ashina', 'Saito', 'Namikawa',
             'Takahara', 'Hosaka'),
            index=None, placeholder="Select your name")
    df_pcs_name = pd.read_csv("pc_specs.csv")["PC"].values
    pc_name = st.selectbox('Input PC name', df_pcs_name,
                           index=None, placeholder="Select PC")
    dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    min_date = dt_now - datetime.timedelta(days=1)
    max_date = dt_now + datetime.timedelta(days=30)
    if name=="Nishio":
        min_date = dt_now - datetime.timedelta(days=180)
        max_date = dt_now + datetime.timedelta(weeks=180)
    col1, col2 = st.columns(2)
    date_start = col1.date_input('Input Start Date', dt_now, min_value=min_date, max_value=max_date)
    time_start = col2.time_input('Input Start Time', dt_now, step=1800)
    col1, col2 = st.columns(2)
    date_end = col1.date_input('Input End Date', dt_now, min_value=min_date, max_value=max_date)
    time_end = col2.time_input('Input End Time', dt_now, step=1800)
    # 名前、PC名が選択されていない場合は、予約ボタンを押せないようにする（warningも出す）
    if name == None or pc_name == None:
        st.warning("Please select your name and PC name.")
        return
    # スタート日時がエンド日時よりも後の場合は、予約ボタンを押せないようにする（warningも出す）
    dt_start = datetime.datetime.combine(date_start, time_start)
    dt_end = datetime.datetime.combine(date_end, time_end)
    if dt_start > dt_end:
        st.warning("Start date is later than end date.")
        return
    # Abaqusの予約の場合、最大で1週間までの予約が可能
    if pc_name == "Abaqus" and (dt_end - dt_start).days > 7 and name != "Nishio":
        st.warning("You can reserve Abaqus for up to 1 week.")
        return
    # Abaqus以外は、最大で30日までの予約が可能
    # 基本的に、カレンダーで押せないようにはしているが、直接入力で抜けることが可能なため、再度確認
    if (dt_end - dt_start).days > 30 and name != "Nishio":
        st.warning("You can reserve for up to 30 days.")
        return
    is_click = st.button("Reserve")
    if is_click:
        reserve(name, pc_name, date_start, time_start, date_end, time_end)

def check_reserve(name, pc_name, date_start, time_start, date_end, time_end):
    """予約可能か確認
    Args:
        name (str): 予約者の名前
        pc_name (str): 予約するPCの名前
        date_start (date): 予約開始日
        time_start (time): 予約開始時刻
        date_end (date): 予約終了日
        time_end (time): 予約終了時刻
    Returns:
        bool: 予約可能かどうか
    """
    dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    dt_start = datetime.datetime.combine(date_start, time_start)
    dt_end = datetime.datetime.combine(date_end, time_end)
    # 時間の差分を時間単位で計算
    diff = (dt_end.replace(tzinfo=ZoneInfo("Asia/Tokyo")) - dt_now).total_seconds() / 3600
    is_one_day = diff <= 24
    # pc_reserves.csvの予約日時と重複していないか確認
    # 重複は、PC名が同じかつ、予約開始日時が予約終了日時よりも前かつ、予約終了日時が予約開始日時よりも後
    read_spreadsheet(is_use_cache=False)
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"])
    df_reserve["End"] = pd.to_datetime(df_reserve["End"])
    df_reserve_check = df_reserve[(df_reserve["PC"] == pc_name) & (df_reserve["Start"] < dt_end) & (dt_start < df_reserve["End"])]
    if len(df_reserve_check) > 0:
        st.error("This PC is already reserved.")
        return False
    if pc_name=="Abaqus":
        return True
    # 同じ予約者がもうすでに予約していないか確認
    df_reserve_check = df_reserve[(df_reserve["User"] == name) & (df_reserve["PC"] != "Abaqus") & (df_reserve["Start"] < dt_end) & (dt_start < df_reserve["End"])]
    # 同じ予約者がもうすでに、一日以上の予約をしているか確認
    is_one_day2 = False
    for index, row in df_reserve_check.iterrows():
        if (row["End"].replace(tzinfo=ZoneInfo("Asia/Tokyo")) - dt_now).total_seconds() / 3600 <= 24:
            is_one_day2 = True
            break
    # すでに二つ以上の予約をしている場合は、予約できない
    if len(df_reserve_check["PC"].unique()) > 1 and name != "Nishio":
        st.error("You already have other reservation.")
        return False
    # すでに一つの予約があり、かつ、一日以上の予約をしている場合は、予約できない
    if len(df_reserve_check["PC"].unique()) > 0 and not is_one_day and not is_one_day2 and name != "Nishio":
        st.error("You already have other reservation.")
        return False
    return True
    
def reserve(name, pc_name, date_start, time_start, date_end, time_end):
    """PCの予約
    Args:
        name (str): 予約者の名前
        pc_name (str): 予約するPCの名前
        date_start (date): 予約開始日
        time_start (time): 予約開始時刻
        date_end (date): 予約終了日
        time_end (time): 予約終了時刻
    Returns:
        _type_: _description_
    """
    with st.spinner('Reserving...'):
        time.sleep(2)
    is_ok = check_reserve(name, pc_name, date_start, time_start, date_end, time_end)
    if not is_ok:
        return
    # 予約
    # pc_reserves.csvに追加
    dt_start = datetime.datetime.combine(date_start, time_start)
    dt_end = datetime.datetime.combine(date_end, time_end)
    df = pd.DataFrame([[pc_name, name, dt_start, dt_end]], columns=["PC", "User", "Start", "End"])
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"])
    df_reserve["End"] = pd.to_datetime(df_reserve["End"])
    df_reserve = pd.concat([df_reserve, df], join='inner')
    df_reserve = df_reserve.reset_index(drop=True)
    # 100件以上の予約情報がある場合は、古い予約情報を削除
    if df_reserve.shape[0]>100:
        df_reserve = df_reserve.drop(range(10))
    df_reserve.to_csv("pc_reserves.csv")
    # print(df_reserve)
    update_spreadsheet()
    # 予約完了メッセージ
    st.success("Reserve Success!")
    # time.sleep(2)

def show_calendar():
    # カレンダーを表示
    st.header("Calendar")
    # df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve = read_spreadsheet()
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve["Start"] = pd.to_datetime(df_reserve["Start"])
    df_reserve["End"] = pd.to_datetime(df_reserve["End"])
    # streamlit_calendarを使う
    calendar_events = []
    for index, row in df_reserve.iterrows():
        # スタートの時刻とエンドの時刻をam、pm形式にして、3:00pm - 5:00pmのように表示する
        start_time = row["Start"].strftime("%I%p")
        end_time = row["End"].strftime("%I%p")
        str_time = start_time + "-" + end_time
        temp = {"title": str_time +" " +row["PC"] + " " + row["User"],
                "start": row["Start"].tz_localize('Asia/Tokyo').strftime("%Y-%m-%dT%H:%M:%S"),
                "end": row["End"].tz_localize('Asia/Tokyo').strftime("%Y-%m-%dT%H:%M:%S")}
        calendar_events.append(temp)
    calendar(calendar_events)

    
def get_pc_reserves():
    """予約情報csvをダウンロードする
    """
    # ダウンロードボタンを押したら、pc_reserves.csvをダウンロードする
    df_reserve = pd.read_csv("pc_reserves.csv")
    df_reserve.to_csv("pc_reserves.csv", index=False)
    with open("pc_reserves.csv", "rb") as file:
        csv = file.read()
    st.download_button(
        label="Download csv",
        data=csv,
        file_name="pc_reserves.csv",
        mime="text/csv"
    )
    
if __name__ == '__main__':
    img_icon = Image.open("icon.jpg")
    st.set_page_config(
        page_title="PC Reserve App",
        page_icon=img_icon
    )
    st.title("PC Reserve System") # タイトル
    is_logined, username = login()
    if is_logined:
        now_using()
        reserve_form()
        show_calendar()
