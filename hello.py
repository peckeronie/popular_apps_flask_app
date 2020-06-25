from flask import Flask, render_template
import sqlite3
import datetime
import time
app = Flask(__name__) #name : current file
example_db = "testappchart.db"

def lookup_database(store, app_category):
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    #latest_id = c.execute('''SELECT id FROM id_table WHERE type=''' + store + ''' AND category=''' + app_category + ''' ORDER BY date DESC;''').fetchone()
    latest_id = c.execute('''SELECT id FROM id_table WHERE type = ? AND category = ? ORDER BY date DESC;''',(store, app_category)).fetchone()
    id_int = int(latest_id[0])
    selected_apps = c.execute('''SELECT name from app_table WHERE info_id = ? ORDER BY rank ASC;''',(id_int,)).fetchall()
    results = []
    for app in selected_apps:
        results.append(str(app[0]))
    conn.commit()
    conn.close()
    return results

@app.route('/') # '/' is default webpage
def hello_world():
    return render_template("home.html")

@app.route("/apple1")
def apple_free_apps():
    store = "iOS"
    type = "Top Free Apps"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/apple2")
def apple_paid_apps():
    store = "iOS"
    type = "Top Paid Apps"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/apple3")
def apple_new_games():
    store = "iOS"
    type = "Top New Games"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/apple4")
def apple_new_apps():
    store = "iOS"
    type = "Top New Apps"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/android1")
def android_free_apps():
    store = "Android"
    type = "Top Free Apps"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/android2")
def android_paid_apps():
    store = "Android"
    type = "Top Paid Apps"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/android3")
def android_free_games():
    store = "Android"
    type = "Top Free Games"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

@app.route("/android4")
def android_paid_games():
    store = "Android"
    type = "Top Paid Games"
    output = lookup_database(store,type)
    return render_template("app_page.html", app_store=store, category=type, app_items=output)

if __name__ == "__main__":
    app.run(debug=True)
