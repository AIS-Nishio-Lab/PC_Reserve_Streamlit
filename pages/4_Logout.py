import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image

if __name__ == "__main__":
    img_icon = Image.open("icon.jpg")
    st.set_page_config(
        page_title="PC Reserve App",
        page_icon=img_icon,
        layout="wide"
    )
    
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
    else:
        st.write("Your username is " + username)
    authenticator.logout('Logout', 'main', key='unique_key')
