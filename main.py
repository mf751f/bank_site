from flask import Flask, render_template, request
import requests
import json

DB = "https://one-piece-bank-default-rtdb.asia-southeast1.firebasedatabase.app/"

def counter():
    counter = json.load(open("static/counter.json", "r"))
    counter["count"] += 1 
    json.dump(fp=open("static/counter.json", "w"), obj=counter)


message = requests.get(f"{DB}/message.json").json()

app = Flask("One Piece Bank", template_folder="temps/", static_folder="static/")

@app.route("/", methods=["GET"])
def home():
    counter()
    code = request.args.get("code")
    if code:
        info = requests.get(f"{DB}/{code}.json").json()
        if info:
            titles = ""
            vip = "Yes" if bool(info["vip"]["is_vip"]) else "No"
            if int(info["archived_titles"]["number"]) < 1:
                titles = "not"
            else :
                if "titles" not in info["archived_titles"]:
                    titles = f"{info['archived_titles']['number']} titles"
                else:
                    for title in info["archived_titles"]["titles"]:
                        titles += f"\'{title}\', "
                    titles = titles[::-1][2:][::-1]
            return render_template("info.html",key_code=code,vip_text=vip,vip_actions = info["vip"]["vip_actions"], at = titles,amino_link=info["amino_link"], amount=info["current_amount"]  )
        return render_template("notFound.html", key_code=code)
    return render_template("index.html", message = message)


app.run(host="0.0.0.0", port=8080)
