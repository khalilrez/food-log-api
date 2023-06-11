from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import HTMLResponse
from typing import Dict,List,Any
from models.food import Food,User,FoodEntry
from datetime import datetime

app = FastAPI()
foods: Dict[int,Food] = {}
food_log: Dict[int, FoodEntry] = {}

HTML_TEMPLATE = """<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Food log for {username}</title>
</head>

<body>
    <table>
        <thead>
            <th>Food</th>
            <th>Added</th>
            <th>Servings</th>
            <th>Calories (kcal)</th>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>

</body>
</html>"""
TABLE_ROW = """<tr>
    <td>{food_name}</td>
    <td>{date_added}</td>
    <td>{number_servings} x {serving_size}</td>
    <td>{total_calories}</td>
</tr>"""



@app.post("/", status_code=201)
async def create_food_entry(entry: FoodEntry):
    if entry.id in food_log:
        raise HTTPException(status_code=400,detail="Food entry already logged, use an update request")
    user = entry.user
    total_calories_today =0
    for x in food_log.values():
        if user.id == x.user.id:
            total_calories_today+= x.total_calories
    if total_calories_today + entry.total_calories > user.max_daily_calories:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot add more food than daily caloric allowance = {user.max_daily_calories} kcal / day",
        )
    food_log[entry.id] = entry
    return entry

@app.get("/users/{user_id}")
def get_user_food_entries(user_id: int) -> List[FoodEntry]:
    user_entries = [entry for entry in food_log.values() if entry.user.id == user_id]
    return user_entries
@app.get("/{username}", response_class=HTMLResponse)
async def show_foods_for_user(request: Request, username: str):
    # 1. extract foods for user using the food_log dict
    # 2. build up the embedded html string
    # 3. return an HTMLResponse (with the html content and status code 200)
    user_entries = [
        entry
        for entry in food_log.values()
        if entry.user.username == username
    ]

    table_rows = ""
    for entry in user_entries:
        table_rows += TABLE_ROW.format(
            food_name=entry.food.name,
            date_added=entry.date_added,
            number_servings = entry.number_servings,
            serving_size = entry.food.serving_size,
            total_calories=entry.total_calories,
        )

    html_content = HTML_TEMPLATE.format(username=user_entries[0].user.username, table_rows=table_rows)
    return HTMLResponse(content=html_content, media_type="text/html")

@app.put("/{entry_id}")
def update_food_entry(entry_id: int, food_entry: FoodEntry):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    food_entry.id = entry_id
    food_log[entry_id] = food_entry
    return food_entry


@app.delete("/{entry_id}")
def delete_food_entry(entry_id: int):
    if entry_id not in food_log:
        raise HTTPException(status_code=404, detail="Food entry not found")
    deleted_entry = food_log.pop(entry_id)
    return {"ok":True}


@app.post("/food", status_code=201)
async def create_food(food: Food):
    try:
        foods[food.id] = food
        return food
    except:
        raise KeyError


# write the two Read endpoints
@app.get("/food/all")
async def read_foods():
    return list(foods.values())

@app.get("/food/{food_id}")
async def read_food(food_id:int):
    try:
        return foods[food_id]
    except:
        raise KeyError

@app.put("/food/{food_id}")
async def update_food(food_id:int,food:Food):
    if food_id not in foods:
        raise HTTPException(status_code=404,detail="Food not found")
    foods[food_id] = food
    return food

@app.delete("/food/{food_id}")
async def delete_food(food_id:int):
    try:
        foods.pop(food_id)
        return {"ok":True}
    except:
        raise HTTPException(status_code=404,detail="Food not found")