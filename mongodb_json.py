import pandas as pd
from pymongo import MongoClient

#Read the csv
data = pd.read_csv("products.csv")
products = data.to_dict("records")

#Mongodb api eky
client = MongoClient("mongodb+srv://admin:password001$@cluster0.qcvivpa.mongodb.net/?appName=Cluster0")

try:
    client.admin.command("ping")
    print("Connected succesfullyyy")
except Exception as e:
    print("Connetion faill", e)
    exit()

#create database and collection
db = client["store"]
collection = db["products"]

#Insert data in nmongo
collection.insert_many(products)
print("products uploaded")