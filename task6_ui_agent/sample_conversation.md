# Sample Conversation – State-Aware UI Agent

This demonstrates:

- UI state manipulation
- State introspection
- Multi-turn conversation (3+ turns)

---

**Turn 1**

**User:**  
show electronics

**Agent:**  
Okay, showing electronics products.  
(Internally: filters.category = 'electronics', view = 'list')

**State after turn 1 (simplified):**

```json
{
  "current_view": "list",
  "selected_product_id": null,
  "filters": {
    "category": "electronics",
    "max_price": null,
    "search_query": null,
    "sort_by": "relevance"
  },
  "cart": []
}
