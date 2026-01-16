from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
import os

app = Flask(__name__)

# Replace with your Supabase credentials
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "your-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    items = supabase.table("requests").select("*").execute().data
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    supabase.table("requests").insert({"text": text}).execute()
    return redirect("/")

@app.route("/toggle/<int:item_id>")
def toggle(item_id):
    # Get current done value
    item = supabase.table("requests").select("*").eq("id", item_id).single().execute().data
    new_done = not item['done']
    supabase.table("requests").update({"done": new_done}).eq("id", item_id).execute()
    return redirect("/")

@app.route("/delete/<int:item_id>")
def delete(item_id):
    supabase.table("requests").delete().eq("id", item_id).execute()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
