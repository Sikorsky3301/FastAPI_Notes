from fastapi import FastAPI 
app = FastAPI()


items = [
    {"id": 1, "AI": "Item 1"},
    {"id": 2, "SDK": "Item 2"},
    {"id": 3, "IDE": "Item 3"},
    {"id": 4, "API": "Item 4"},
    {"id": 5, "AGENT": "Item 5"},
]
@app.get("/health")
def health_check():
    return {"status": "ok"}
    
@app.get("/items")
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}