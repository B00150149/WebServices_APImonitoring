from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
# from prometheus_fastapi_instrumentator import Instrumentator
import requests


app = FastAPI()

# instrumentator = Instrumentator()
# instrumentator.instrument(app).expose(app)

client = MongoClient("mongodb+srv://admin:password001$@cluster0.qcvivpa.mongodb.net/?appName=Cluster0")

try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Connection failed:", e)
    exit()



# Create DB + collection
db = client["store"]
collection = db["products"]

class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str

@app.get("/getAll")
def getAll():
    products = list(collection.find({}, {"_id" : 0}))
    return products

@app.get("/getSingleProduct/{product_ID}")
def getSingleProduct(product_ID: int):

    product = list(collection.find({"ProductID": product_ID}, {"_id" : 0}))
    if product:
        return product
    else:
        return {"message": "Product not founddd"}


@app.post("/addNew")
def addNew(product: Product):

    collection.insert_one(product.dict())
    return {"message": "New product added succesfulluy"}


@app.delete("/deleteOne/{product_ID}")
def deleteOne(product_ID: int):

    deleted = collection.delete_one({"ProductID": product_ID})

    if deleted.deleted_count == 1:
        return {"message": "product deleted"}
    else:
        return {"message": "Product not found"}
    

@app.get("/startsWith/{letter}")
def startsWith(letter: str):

    products = list(collection.find({"Name": {"$regex": f"^{letter}", "$options": "i"}}, {"_id" : 0}))
    return products


@app.get("/paginate")
def paginate(start_id: int, end_id:int):

    products = list(collection.find({"ProductID": {"$gte": start_id, "$lte": end_id}}, {"_id" : 0}).limit(10))
    return products


@app.get("/convert/{product_ID}")
def convert(product_ID: int):

    product = collection.find_one({"ProductID": product_ID})

    if not product:
        return {"message": "Product not founddd"}
    
    price_usd = product["UnitPrice"]
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    euro_rate = data["rates"]["EUR"]
    price_euro = price_usd * euro_rate

    return {
        "ProductID": product_ID,
        "PriceUSD": price_usd,
        "PriceEUR": round(price_euro, 2)
    }