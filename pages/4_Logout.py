import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth

if __name__ == "__main__":
    
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