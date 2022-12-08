from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductItem:
    name: Optional[int] = None
    url: Optional[int] = None
    price: Optional[str] = None
    discounted_price: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
