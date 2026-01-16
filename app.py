from flask import Flask, render_template, request, redirect
from supabase import create_client
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    items = supabase.table("requests").select("*").order("id").execute().data
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    supabase.table("requests").insert({"text": text, "done": False}).execute()
    return redirect("/")

@app.route("/toggle/<int:item_id>")
def toggle(item_id):
    item = supabase.table("requests").select("done").eq("id", item_id).single().execute().data
    supabase.table("requests").update({"done": not item["done"]}).eq("id", item_id).execute()
    return redirect("/")

@app.route("/delete/<int:item_id>")
def delete(item_id):
    supabase.table("requests").delete().eq("id", item_id).execute()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
