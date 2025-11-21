from __future__ import annotations

from typing import Tuple

from ui_state import UIState, CartItem, FilterState


# Small in-memory "catalog" for demo
CATALOG = {
    "p1": CartItem(product_id="p1", name="iPhone 15", price=80000.0),
    "p2": CartItem(product_id="p2", name="Samsung Galaxy S24", price=70000.0),
    "p3": CartItem(product_id="p3", name="Boat Airpods", price=2500.0),
    "p4": CartItem(product_id="p4", name="Dell Laptop", price=55000.0),
}


class UIAgent:
    """
    Simple state-aware e-commerce assistant.

    - Maintains a UIState object.
    - Parses user commands.
    - Updates the state.
    - Always responds based on *current* state (introspection).
    """

    def __init__(self, initial_state: UIState | None = None) -> None:
        self.state: UIState = initial_state or UIState()

    # ----------------------
    # Public interface
    # ----------------------
    def handle_user_message(self, message: str) -> Tuple[str, UIState]:
        """
        Main entrypoint. Takes a user message, updates state, and returns:
        - agent_reply (str)
        - updated_state (UIState)
        """
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

    # ----------------------
    # Internal helpers
    # ----------------------
    def _go_to_cart(self) -> str:
        self.state.current_view = "cart"
        if not self.state.cart:
            return "Your cart is empty right now. You can say 'add iPhone' or 'add laptop'."

        lines = [f"You have {self.state.total_items()} item(s) in your cart:"]
        for item in self.state.cart:
            lines.append(
                f"- {item.name} (x{item.quantity}) — ₹{item.price * item.quantity:.2f}"
            )
        lines.append(f"Total: ₹{self.state.total_price():.2f}")
        return "\n".join(lines)

    def _add_item_from_text(self, text: str) -> str:
        # very simple keyword map
        if "iphone" in text:
            product = CATALOG["p1"]
        elif "samsung" in text or "galaxy" in text:
            product = CATALOG["p2"]
        elif "airpods" in text or "earbuds" in text:
            product = CATALOG["p3"]
        elif "laptop" in text or "dell" in text:
            product = CATALOG["p4"]
        else:
            return "I couldn't match that product. Try: add iphone / add samsung / add airpods / add laptop."

        # check if already in cart
        for item in self.state.cart:
            if item.product_id == product.product_id:
                item.quantity += 1
                self.state.current_view = "cart"
                return (
                    f"Added one more {product.name} to your cart. "
                    f"Now you have {item.quantity} of them. "
                    f"Cart total is ₹{self.state.total_price():.2f}."
                )

        # not in cart yet → add new
        self.state.cart.append(CartItem(**product.model_dump()))
        self.state.current_view = "cart"
        return (
            f"Added {product.name} to your cart. "
            f"You now have {self.state.total_items()} item(s) in the cart. "
            f"Cart total is ₹{self.state.total_price():.2f}."
        )

    def _remove_item_from_text(self, text: str) -> str:
        if not self.state.cart:
            return "Cart is already empty mowa. Nothing to remove."

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
            return "I couldn't figure out which item to remove. Try: remove iphone / remove laptop."

        before = len(self.state.cart)
        self.state.cart = [item for item in self.state.cart if item.product_id != target_id]
        after = len(self.state.cart)

        if before == after:
            return "That item is not in your cart mowa."
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
            return "You can't checkout with an empty cart mowa. Try adding something first."

        self.state.current_view = "checkout"
        return (
            f"Moving to checkout page.\n"
            f"You have {self.state.total_items()} item(s) with total ₹{self.state.total_price():.2f}."
        )

    def _introspect_state(self) -> str:
        """
        This is the 'state introspection' demo.

        The agent explains what it thinks the UI state is right now.
        """
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


if __name__ == "__main__":
    # Simple manual test loop
    agent = UIAgent()
    print("E-commerce UI Agent. Type 'exit' to quit.\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break
        reply, state = agent.handle_user_message(user)
        print("\nAgent:\n" + reply)
        print("\n[DEBUG UI STATE]", state.model_dump())
        print("\n" + "-" * 60 + "\n")
