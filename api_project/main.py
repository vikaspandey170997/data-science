from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor

from database import get_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


class LoginRequest(BaseModel):
    emailID: str
    password: str


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: Decimal = Field(default=Decimal("0"), ge=0)


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal


users = [
    {"email": "Don@google.com", "password": "Don@123"}
]


@app.get("/")
def read_root():
    return {"message": "API is running"}


@app.post("/authentication")
def authenticate(request: LoginRequest):
    for user in users:
        if user["email"] == request.emailID and user["password"] == request.password:
            return {"authenticated": True}
    return {"message": "User not found"}


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: PgConnection = Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            INSERT INTO items (name, description, price)
            VALUES (%s, %s, %s)
            RETURNING id, name, description, price;
            """,
            (item.name, item.description, item.price),
        )
        return cursor.fetchone()


@app.get("/items", response_model=list[ItemResponse])
def list_items(db: PgConnection = Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT id, name, description, price
            FROM items
            ORDER BY id;
            """
        )
        return cursor.fetchall()


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: PgConnection = Depends(get_db)):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            SELECT id, name, description, price
            FROM items
            WHERE id = %s;
            """,
            (item_id,),
        )
        item = cursor.fetchone()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: PgConnection = Depends(get_db)):
    update_data = item.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field is required",
        )

    allowed_fields = {"name", "description", "price"}
    assignments = ", ".join(f"{field} = %s" for field in update_data if field in allowed_fields)
    values = list(update_data.values())
    values.append(item_id)

    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
            UPDATE items
            SET {assignments}
            WHERE id = %s
            RETURNING id, name, description, price;
            """,
            values,
        )
        updated_item = cursor.fetchone()

    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return updated_item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: PgConnection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
        deleted_count = cursor.rowcount

    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
