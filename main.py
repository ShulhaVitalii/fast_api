from enum import Enum
from typing import Union, Annotated

from fastapi import FastAPI, Query, Path, Body

from models import Item, User, Offer, Image


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user")
def get_all_users():
    return {"users": {}}


@app.get("/user/{user_id}")
def get_all_users(user_id: int):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Query Parameters
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip+limit]


# async def read_item(item_id: str, q: str | None = None):   available in 3.10+
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Request Body
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result


# Query Parameters and String Validations
@app.get("/items/")
# async def read_items(q: Annotated[Union[str, None], Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
async def read_items(
        q: Annotated[str, Query(
            title="Query string",
            description="Query string for the items to search in the database that"
                        " have a good match",
            min_length=3,
            max_length=50
        )] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Path Parameters and Numeric Validations
# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal
@app.get("/item/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=100)],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Body - Multiple Parameters
@app.put("/itemss/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: Union[str, None] = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# Body - Fields
# Body - Nested Models
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
