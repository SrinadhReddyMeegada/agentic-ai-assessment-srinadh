from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import json
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from ui_state import UIState, CartItem, FilterState

app = FastAPI(title="Task 6 – State-Aware UI Agent (Web)")


# ----------------------
# Simple in-memory agent
# ----------------------


CATALOG = {
    "p1": CartItem(product_id="p1", name="iPhone 15", price=80000.0),
    "p2": CartItem(product_id="p2", name="Samsung Galaxy S24", price=70000.0),
    "p3": CartItem(product_id="p3", name="Boat Airpods", price=2500.0),
    "p4": CartItem(product_id="p4", name="Dell Laptop", price=55000.0),
}


class UIAgent:
    """
    Simple state-aware e-commerce assistant for the web UI.

    - Maintains a UIState object.
    - Parses user commands.
    - Updates the state.
    - Returns reply + updated state.
    """

    def __init__(self, initial_state: Optional[UIState] = None) -> None:
        self.state: UIState = initial_state or UIState()

    def handle_user_message(self, message: str) -> Tuple[str, UIState]:
        text = message.strip().lower()

        if any(word in text for word in ["show", "browse", "see"]) and "cart" in text:
            reply = self._go_to_cart()
        elif text.startswith("add "):
            reply = self._add_item_from_text(text)
        elif text.startswith("remove "):
            reply = self._remove_item_from_text(text)
        elif "electronics" in text:
            reply = self._set_category("electronics")
        elif "mobiles" in text or "phones" in text:
            reply = self._set_category("mobiles")
        elif "clear filters" in text:
            reply = self._clear_filters()
        elif "checkout" in text:
            reply = self._go_to_checkout()
        elif "state" in text and "show" in text:
            reply = self._introspect_state()
        else:
            reply = self._generic_help()

        return reply, self.state

    # --- Internal helpers ---

    def _go_to_cart(self) -> str:
        self.state.current_view = "cart"
        if not self.state.cart:
            return "Your cart is empty right now. You can type 'add iphone' or 'add laptop'."

        lines = [f"You have {self.state.total_items()} item(s) in your cart:"]
        for item in self.state.cart:
            lines.append(
                f"- {item.name} (x{item.quantity}) — ₹{item.price * item.quantity:.2f}"
            )
        lines.append(f"Total: ₹{self.state.total_price():.2f}")
        return "\n".join(lines)

    def _add_item_from_text(self, text: str) -> str:
        if "iphone" in text:
            product = CATALOG["p1"]
        elif "samsung" in text or "galaxy" in text:
            product = CATALOG["p2"]
        elif "airpods" in text or "earbuds" in text:
            product = CATALOG["p3"]
        elif "laptop" in text or "dell" in text:
            product = CATALOG["p4"]
        else:
            return (
                "I couldn't match that product. Try: "
                "add iphone / add samsung / add airpods / add laptop."
            )

        for item in self.state.cart:
            if item.product_id == product.product_id:
                item.quantity += 1
                self.state.current_view = "cart"
                return (
                    f"Added one more {product.name} to your cart. "
                    f"Now you have {item.quantity} of them. "
                    f"Cart total is ₹{self.state.total_price():.2f}."
                )

        self.state.cart.append(CartItem(**product.model_dump()))
        self.state.current_view = "cart"
        return (
            f"Added {product.name} to your cart. "
            f"You now have {self.state.total_items()} item(s) in the cart. "
            f"Cart total is ₹{self.state.total_price():.2f}."
        )

    def _remove_item_from_text(self, text: str) -> str:
        if not self.state.cart:
            return "Cart is already empty. Nothing to remove."

        target_id = None
        if "iphone" in text:
            target_id = "p1"
        elif "samsung" in text or "galaxy" in text:
            target_id = "p2"
        elif "airpods" in text or "earbuds" in text:
            target_id = "p3"
        elif "laptop" in text or "dell" in text:
            target_id = "p4"

        if target_id is None:
            return (
                "I couldn't figure out which item to remove. "
                "Try: remove iphone / remove samsung / remove laptop."
            )

        before = len(self.state.cart)
        self.state.cart = [item for item in self.state.cart if item.product_id != target_id]
        after = len(self.state.cart)

        if before == after:
            return "That item is not in your cart."
        else:
            self.state.current_view = "cart"
            if not self.state.cart:
                return "Removed it. Your cart is now empty."
            return (
                "Removed it from your cart. "
                f"You now have {self.state.total_items()} item(s). "
                f"Current cart total is ₹{self.state.total_price():.2f}."
            )

    def _set_category(self, category: str) -> str:
        self.state.current_view = "list"
        self.state.filters.category = category
        return (
            f"Okay, showing {category} products.\n"
            f"(Internally: filters.category = '{self.state.filters.category}', "
            f"view = '{self.state.current_view}')"
        )

    def _clear_filters(self) -> str:
        self.state.filters = FilterState()
        return "Cleared all filters. Showing all products again."

    def _go_to_checkout(self) -> str:
        if not self.state.cart:
            return "You can't checkout with an empty cart. Try adding something first."

        self.state.current_view = "checkout"
        return (
            f"Moving to checkout page.\n"
            f"You have {self.state.total_items()} item(s) with total ₹{self.state.total_price():.2f}."
        )

    def _introspect_state(self) -> str:
        lines = [
            f"Current view: {self.state.current_view}",
            f"Selected product: {self.state.selected_product_id or 'None'}",
            f"Cart items: {self.state.total_items()} (₹{self.state.total_price():.2f})",
            f"Active category filter: {self.state.filters.category or 'None'}",
            f"Search query: {self.state.filters.search_query or 'None'}",
            f"Sort by: {self.state.filters.sort_by}",
        ]
        return "\n".join(lines)

    def _generic_help(self) -> str:
        return (
            "I can help you manage your shopping UI. Try things like:\n"
            "- 'show electronics'\n"
            "- 'add iphone'\n"
            "- 'show cart'\n"
            "- 'remove laptop'\n"
            "- 'checkout'\n"
            "- 'show state' (to see internal UI state)"
        )


# Single global agent for this simple demo.
agent = UIAgent()


# ----------------------
# Routes
# ----------------------


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main HTML page."""
    html_path = Path(__file__).parent / "index.html"
    html = html_path.read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.post("/message", response_class=HTMLResponse)
async def handle_message(message: str = Form(...)) -> HTMLResponse:
    """
    HTMX endpoint for chat messages.

    Returns an HTML snippet that HTMX will append to the chat area.
    Also triggers a state refresh via embedded script.
    """
    reply, state = agent.handle_user_message(message)

    # Simple HTML snippet containing user + agent messages.
    # HTMX will append this to #chat-log.
    snippet = f"""
    <div class="chat-block">
      <div class="msg user"><strong>You:</strong> {message}</div>
      <div class="msg agent"><strong>Agent:</strong> {reply.replace('\n', '<br>')}</div>
    </div>
    <script>
      htmx.ajax('GET', '/state', '#state-panel');
    </script>
    """
    return HTMLResponse(snippet)


@app.get("/state", response_class=HTMLResponse)
async def get_state() -> HTMLResponse:
    """
    Returns the current UI state as pretty-printed JSON inside <pre>.
    HTMX swaps this into the state panel.
    """
    state_json = json.dumps(agent.state.model_dump(), indent=2)
    html = f"<pre>{state_json}</pre>"
    return HTMLResponse(html)


@app.get("/health", response_class=PlainTextResponse)
async def health() -> PlainTextResponse:
    return PlainTextResponse("ok")
