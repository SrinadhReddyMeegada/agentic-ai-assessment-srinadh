from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class FilterState(BaseModel):
    """Represents active filters in the e-commerce UI."""
    category: Optional[str] = Field(
        default=None, description="Active product category filter, e.g. 'electronics'"
    )
    max_price: Optional[float] = Field(
        default=None, description="Maximum price filter for visible products"
    )
    search_query: Optional[str] = Field(
        default=None, description="Free-text search query"
    )
    sort_by: str = Field(
        default="relevance",
        description="Sort order: 'relevance', 'price_low_high', 'price_high_low'",
    )


class CartItem(BaseModel):
    """A single item in the shopping cart."""
    product_id: str
    name: str
    price: float
    quantity: int = 1


class UIState(BaseModel):
    """
    Global UI state for the e-commerce agent.

    This is what the agent "sees" and manipulates.
    """
    current_view: str = Field(
        default="home",
        description="Current page: 'home', 'list', 'details', 'cart', 'checkout'",
    )
    selected_product_id: Optional[str] = Field(
        default=None, description="Currently selected product id, if any"
    )
    filters: FilterState = Field(
        default_factory=FilterState,
        description="Current active filters",
    )
    cart: List[CartItem] = Field(
        default_factory=list,
        description="Items currently in the cart",
    )

    def total_items(self) -> int:
        """Return total number of units in the cart."""
        return sum(item.quantity for item in self.cart)

    def total_price(self) -> float:
        """Return total price of all items in the cart."""
        return sum(item.price * item.quantity for item in self.cart)
