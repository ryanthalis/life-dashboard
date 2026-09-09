from fastapi import FastAPI, HTTPException, Path, Query
from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints
from datetime import date
import db

    

app = FastAPI()

class EntryCreate(BaseModel):
    entry_date: date
    category: Literal["workout", "study"]
    label: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    quantity: Annotated[int, Field(gt=0)]
    notes: str = ""

class EntryResponse(EntryCreate):
    id: Annotated[int, Field(gt=0)]

class EntryUpdate(BaseModel):
    entry_date: date | None = None
    category: Literal["workout", "study"] | None = None
    label: Annotated[str | None, StringConstraints(min_length=1, strip_whitespace=True)] = None
    quantity: Annotated[int | None, Field(gt=0)] = None
    notes: str | None = None

def handle_row_formatting(i):

    values = ({"id": i["id"], "entry_date": i["entry_date"], "category": i["category"], "label": i["label"], 
        "quantity": i["quantity"], "notes": i["notes"]})

    return values

@app.get("/")
def read_root():
    return {"message": "Life Dashboard API"}

@app.get("/entries/{entry_id}", response_model=EntryResponse)
def read_entry(entry_id: Annotated[int, Path(gt=0)]):
    entry = db.get_entry(entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry: {entry_id} was not found") 

    values = handle_row_formatting(entry)

    return values

@app.get("/entries", response_model=list[EntryResponse])
def read_entries(category: Annotated[str | None, Query(pattern=r"^(workout|study)$")] = None):


    rows = db.get_entries(category)

    values = []

    if len(rows) == 0:
        return values
    
    for i in rows:
        values.append(handle_row_formatting(i))
    
    return values

@app.post("/entries", status_code=201, response_model=EntryResponse)
def post_entry(entry: EntryCreate) -> dict[str, str | int]:
    
    entryID = db.add_entry(entry.entry_date.isoformat(), entry.category, entry.label, entry.quantity, entry.notes)
    row = db.get_entry(entryID)

    return handle_row_formatting(row)

@app.patch("/entries/{entry_id}", response_model=EntryResponse)
def patch_entry(entry_id: Annotated[int, Path(gt=0)], updated_entry: EntryUpdate) -> dict[str, str | int]:

    current = db.get_entry(entry_id)

    if current is None:
        raise HTTPException(status_code=404, detail="Row does not exist")

    current = dict(current)

    new = updated_entry.model_dump(exclude_unset=True, exclude_none = True, mode="json")

    current.update(new)

    db.update_entry(current["id"], current["entry_date"], current["category"], current["label"], current["quantity"],
                    current["notes"])

    current = dict(db.get_entry(entry_id))

    return handle_row_formatting(current)

@app.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: Annotated[int, Path(gt=0)]) -> None:

    if db.delete_entry(entry_id):
        return None
    else:
        raise HTTPException(status_code=404, detail="Entry was not found")
    
