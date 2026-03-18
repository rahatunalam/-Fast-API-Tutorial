from fastapi import FastAPI, Path ,Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel
#python -m uvicorn main:app --reload

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {
    1:{
        "name": "Milk",
        "price": 3.99,
        "brand": "Reguler"
    }
}

#Path Parameters
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(..., description="The item you would like to view.",gt=0)):
    return inventory[item_id]

#Query parameter
@app.get("/get-by-name/{item_id}")
def get_item(*, item_id:  int, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail= "Item name not found")
#http://127.0.0.1:8000/get-by-name?test=2&name=Milk

@app.post("/create-item/{item_id}")
def create_item(item_id: int,item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400 , detail="Item Already exist.")
    inventory[item_id] = {"name": item.name,"price": item.price,"brand": item.brand}
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404,detail="Item ID does not exist.")
    
    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None: 
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(...,description="The ID of the item to delete"), gt=0):
    if item_id in inventory:
        raise HTTPException(status_code="ID does not exsit.")
    
    del inventory[item_id]
    return {"Success": "Item deleted!"}
