import subprocess
import sys

import requests

if len(sys.argv) > 1:
    username_pasword = sys.argv[1]
else:
    username_pasword = "stringaas"

data = {"username": username_pasword, "password": username_pasword}
url = "http://127.0.0.1:8000/auth/login/"

response = requests.post(url, data=data).json()

token = "Bearer " + response["access"]

subprocess.run(["xclip", "-selection", "clipboard"], input=token.encode("utf-8"))
