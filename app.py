from flask import Flask, render_template, request, redirect
from supabase import create_client
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    response = supabase.table("requests") \
        .select("*") \
        .eq("is_archived", False) \
        .order("id", desc=True) \
        .execute()

    items = response.data or []
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    text = request.form["text"]
    name = request.form.get("name")

    supabase.table("requests").insert({
        "text": text,
        "name": name
    }).execute()

    return redirect("/")

@app.route("/pray/<int:item_id>")
def pray(item_id):
    item = supabase.table("requests") \
        .select("prayed_count") \
        .eq("id", item_id) \
        .single() \
        .execute()

    count = item.data["prayed_count"] or 0

    supabase.table("requests") \
        .update({"prayed_count": count + 1}) \
        .eq("id", item_id) \
        .execute()

    return redirect("/")

@app.route("/toggle/<int:item_id>")
def toggle(item_id):
    item = supabase.table("requests").select("done").eq("id", item_id).single().execute().data
    supabase.table("requests").update({"done": not item["done"]}).eq("id", item_id).execute()
    return redirect("/")

@app.route("/archive/<int:item_id>")
def archive(item_id):
    supabase.table("prayers") \
        .update({"is_archived": True}) \
        .eq("id", item_id) \
        .execute()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
