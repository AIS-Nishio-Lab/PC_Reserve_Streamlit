from github import Github
import dropbox
import streamlit as st

def get_pc_reserve_csv_from_github():
    ## リポジトリのURL
    #repo_name = "AIS-Nishio-Lab/PC_Reserve_Streamlit"
    #file_name = "pc_reserves.csv"
    #token = "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"
    #g = Github(token)
    #repo = g.get_repo(repo_name)
    #contents = repo.get_contents(file_name)
    #content = contents.decoded_content.decode("utf-8")
    ## ファイルを保存
    #with open(file_name, "w") as f:
    #    f.write(content)
    # 
    # dropboxに変更
    token = "sl.BxSRbl854fPC-1EHzeMb8HIecaZ3i5j2pkLELV-f_9jyOBFy93YwajytUmtux3NvH1_2xwQsotVwcYvWUUYMExFboVSCkJwn8SzBYMofwiAoBC2V764CyO_3vXb94cnS_Wauj6n83JOzgEaI5Yn2"
    st.write(token)
    dbx = dropbox.Dropbox(token)
    with open('pc_reserves.csv', "wb") as f:
        metadata, res = dbx.files_download(path="/pc_reserves.csv")
        f.write(res.content)

def write_pc_reserve_csv_to_github():
    ## リポジトリのURL
    #repo_name = "AIS-Nishio-Lab/PC_Reserve_Streamlit"
    #file_name = "pc_reserves.csv"
    #token = "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"
    #g = Github(token)
    #repo = g.get_repo(repo_name)
    ## csvファイルをエンコード
    #with open("pc_reserves.csv", "r") as file:
    #    csv = file.read()
    #update_file_class = repo.get_contents(file_name)
    #repo.update_file(file_name, "update pc_reserves.csv", csv, update_file_class.sha)
    #
    # dropboxに変更
    token = "sl.BxSRbl854fPC-1EHzeMb8HIecaZ3i5j2pkLELV-f_9jyOBFy93YwajytUmtux3NvH1_2xwQsotVwcYvWUUYMExFboVSCkJwn8SzBYMofwiAoBC2V764CyO_3vXb94cnS_Wauj6n83JOzgEaI5Yn2"
    dbx = dropbox.Dropbox(token)
    with open('pc_reserves.csv', "rb") as f:
        dbx.files_upload(f.read(), "/pc_reserves.csv", mode=dropbox.files.WriteMode.overwrite)
