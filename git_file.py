from github import Github

def get_pc_reserve_csv_from_github():
    # リポジトリのURL
    repo_name = "AIS-Nishio-Lab/PC_Reserve_Streamlit"
    file_name = "pc_reserves.csv"
    token = "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"
    g = Github(token)
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(file_name)
    content = contents.decoded_content.decode("utf-8")
    # ファイルを保存
    with open(file_name, "w") as f:
        f.write(content)

def write_pc_reserve_csv_to_github():
    # リポジトリのURL
    repo_name = "AIS-Nishio-Lab/PC_Reserve_Streamlit"
    file_name = "pc_reserves.csv"
    token = "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"
    g = Github(token)
    repo = g.get_repo(repo_name)
    # csvファイルをエンコード
    with open("pc_reserves.csv", "r") as file:
        csv = file.read()
    update_file_class = repo.get_contents(file_name)
    repo.update_file(file_name, "update pc_reserves.csv", csv, update_file_class.sha)
