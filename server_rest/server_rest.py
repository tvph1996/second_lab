from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

class Item(BaseModel):
    id: int
    name: str

fastApiApp = FastAPI()


itemsData: dict[int, Item] = {
    1: Item(id=1, name="Table")
}


@fastApiApp.get("/items/{itemId}", response_model=Item)
def GetItemPerformanceTest(itemId: int):
    if itemId in itemsData:
        return itemsData[itemId]
        
    else:
        raise HTTPException(status_code=404, detail=f"Item with id {itemId} not found.")


@fastApiApp.post("/items/", response_model=Item)
def AddItemPerformanceTest(item: Item):
    
    if item.id == 100000:
        itemsData[item.id] = item  
        return item


if __name__ == '__main__':
    uvicorn.run(fastApiApp, host='0.0.0.0', port=8000)