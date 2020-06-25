#create the database and fill it daily with new top trending apps from the iOS and Google Play store

import sqlite3
import datetime
import time
import schedule
import requests
from bs4 import BeautifulSoup
example_db = "testappchart.db"

# id_table:
# id: a unique number for each entry
# date: a timestamp for the day that the apps were retrieved
# type: iOS or Android
# category: category of app (ex: free, paid, games)

# app_table:
# info_id: a number corresponding to an entry in the id_table
# rank: the popularity rank of the app
# name: the name of the app
def create_database():
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    #c.execute('''CREATE TABLE IF NOT EXISTS id_table (id int, date text, type text, category text);''')
    c.execute('''CREATE TABLE IF NOT EXISTS id_table (id int, date timestamp, type text, category text);''')
    c.execute('''CREATE TABLE IF NOT EXISTS app_table (info_id int, rank int, name text);''')
    conn.commit() # commit commands
    conn.close() # close connection to database

#after getting the top apps in a specific category, insert a new entry
def insert_into_database(app_store, category, app_list):
    x = datetime.datetime.now()
    #day = x.strftime("%x") #get a date representation as a string
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    latest_id = c.execute('''SELECT id from id_table ORDER BY id DESC;''').fetchone()
    if latest_id == None:
        latest_id = 0
    else:
        latest_id = latest_id[0] + 1

    c.execute('''INSERT into id_table VALUES (?,?,?,?);''',(latest_id,x,app_store,category))
    for rank, app_name in enumerate(app_list, start=1):
        c.execute('''INSERT into app_table VALUES (?,?,?);''',(latest_id,rank,app_name))
    conn.commit()
    conn.close()
    print("Insert into database completed")

def lookup_database(): #for testing
    conn = sqlite3.connect(example_db)
    c = conn.cursor()
    things = c.execute('''SELECT * FROM id_table ORDER BY date DESC;''').fetchall()
    for row in things:
        print(row)
    print("Category table completed")
    apps = c.execute('''SELECT * FROM app_table ORDER BY info_id DESC;''').fetchall()
    for x in apps:
        print(x)
    conn.commit()
    conn.close()
    print("Lookup completed")

#get top iOS apps for a specific category
def get_RSS_feed(category, url):
    r = requests.get(url)
    data = r.json()
    r.close()
    results = data["feed"]["results"]
    out = []

    for item in results:
        #print(count, item["name"])
        out.append(item["name"])
    insert_into_database("iOS", category, out)


#get top Google Play apps for a specific category
def get_HTML_feed(category_name):
    r = requests.get("https://play.google.com/store/apps/top")
    html = BeautifulSoup(r.text, "html.parser")
    r.close()
    all_categories = html.findAll("h2")
    out = []
    for i in all_categories:
        if (i.text.strip() == category_name):
            div_parent = i.parent.parent.parent.parent
            all_children = div_parent.findChildren("div" , recursive=False)
            apps_element = all_children[1] #div_class = ZmHEEd
            apps = apps_element.findAll("div", recursive=False) #div_class = WHE7ib

            for item in apps:
                x = item.find("div").find("div").findAll("div", recursive=False)[1].find("div") #div_class = vU6FJ
                app_name = x.find("div").find("div").find("div").find("div").find("div").find("a").find("div")
                #print(count, app_name["title"])
                out.append(app_name["title"])

            insert_into_database("Android", category_name, out)
            break


#4 categories for iOS
def set_category(category_name):
    begin = r"https://rss.itunes.apple.com/api/v1/us/ios-apps/"
    end = r"/all/10/explicit.json"
    if category_name == 'Top Free Apps':
        begin = begin + "top-free" + end
    elif category_name == 'Top Paid Apps':
        begin = begin + "top-paid" + end
    elif category_name == "Top New Games":
        begin = begin + "new-games-we-love" + end
    elif category_name == "Top New Apps":
        begin = begin + "new-apps-we-love" + end
    return begin

def daily_task():
    apple_categories = ["Top Free Apps", "Top Paid Apps", "Top New Games", "Top New Apps"]
    for c in apple_categories:
        url_name = set_category(c)
        get_RSS_feed(c, url_name)

    google_categories = ["Top Free Apps", "Top Paid Apps", "Top Free Games", "Top Paid Games"]
    for g in google_categories:
        get_HTML_feed(g)

#add new entries to database every midnight
schedule.every().day.at("00:00").do(daily_task)

while True:
    schedule.run_pending()
    time.sleep(60)
#daily_task()
# lookup_database()

##test = set_category("Top Free Apps")
##get_RSS_feed("Top Free Apps", test)
##lookup_database()
##get_HTML_feed("Top Paid Apps")
##get_HTML_feed("Top Free Games")
##
##test = set_category("Top Paid Apps")
##get_RSS_feed("Top Paid Apps", test)
##test2 = set_category("Top New Games")
##get_RSS_feed("Top New Games", test2)
##lookup_database()
