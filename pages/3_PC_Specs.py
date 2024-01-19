import streamlit as st
import streamlit_authenticator as stauth
from streamlit_calendar import calendar
from st_mui_dialog import st_mui_dialog
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from PIL import Image

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
        
def show_pc_specs():
    # PCの仕様を表示
    st.header("PC Specs")
    df_pcs = pd.read_csv("pc_specs.csv")
    st.table(df_pcs)
    
def edit_pc_specs():
    # PCの仕様を編集
    st.header("Edit PC Specs")
    on = st.toggle('Show Edit Form', False)
    if not on:
        return
    df_pcs = pd.read_csv("pc_specs.csv")
    edited = st.data_editor(df_pcs, num_rows="dynamic")
    is_click = st_mui_dialog(title="Confirmation", content="Please confirm that you want to save the changes", 
                            button_txt="Save Edited Data")
    # 編集された場合は、csvに保存
    if is_click:
        edited.to_csv("pc_specs.csv", index=False)
        st.success("Save Success!")

if __name__ == '__main__':
    img_icon = Image.open("icon.jpg")
    st.set_page_config(
        page_title="PC Reserve App",
        page_icon=img_icon
    )
    st.title("PC Reserve System") # タイトル
    is_logined, username = login()
    if is_logined:
        show_pc_specs()
    if is_logined and username=="admin":
        st.header("This section is only for admin")
        edit_pc_specs()
