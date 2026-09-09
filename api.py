from fastapi import FastAPI, HTTPException, Path, Query
from typing import Annotated
from pydantic import BaseModel

import db

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Life Dashboard API"}

@app.get("/entries/{entry_id}")
def read_entry(entry_id: Annotated[int, Path(gt=0)]):
    entry = db.get_entry(entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry: {entry_id} was not found") 

    values = handle_row_formatting(entry)

    return values

@app.get("/entries")
def read_entries(category: Annotated[str | None, Query(pattern=r"^(workout|study)$")] = None):


    rows = db.get_entries(category)

    values = []

    if len(rows) == 0:
        return values
    
    for i in rows:
        values.append(handle_row_formatting(i))
    
    return values

def handle_row_formatting(i):

    values = ({"ID": i["id"], "Date": i["entry_date"], "Category": i["category"], "Label": i["label"], 
        "Quantity": i["quantity"], "Notes": i["notes"]})

    return values