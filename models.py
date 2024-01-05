from typing import Union

from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="Price must be greater than zero")
    tax: Union[float, None] = None
    tags: set[str] = set()
    images: Union[list[Image], None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": ["first_tag", "second_tag"],
                    "images": [
                        {
                            "url": "https://example.com/",
                            "name": "img_name"
                        }
                    ]
                }
            ]
        }
    }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
