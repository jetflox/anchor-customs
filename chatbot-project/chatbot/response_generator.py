"""
Response Generator.
Formats chatbot responses based on intent and search results.
"""

import random
from .training_data import STATIC_RESPONSES


class ResponseGenerator:
    def format_product_card(self, product):
        """Format a single product as an HTML card."""
        badge_html = ""
        if product.get('badge'):
            badge_html = f'<span class="badge">{product["badge"]}</span>'

        original_price_html = ""
        if product.get('originalPrice') and product['originalPrice'] != product['price']:
            original_price_html = f'<span class="original-price">&#8377;{product["originalPrice"]:,}</span>'

        includes_html = ""
        if product.get('includes'):
            items = ", ".join(product['includes'])
            includes_html = f'<div class="includes">Includes: {items}</div>'

        savings_html = ""
        if product.get('savings'):
            savings_html = f'<span class="savings">Save &#8377;{product["savings"]}</span>'

        return f'''<div class="product-card">
            <div class="product-header">
                <strong>{product["name"]}</strong> {badge_html}
            </div>
            <div class="product-desc">{product.get("description", "")}</div>
            {includes_html}
            <div class="product-price">
                {original_price_html}
                <span class="current-price">&#8377;{product["price"]:,}</span>
                {savings_html}
            </div>
        </div>'''

    def generate(self, intent, search_results=None, price_filters=None, all_products=None, all_combos=None):
        """Generate a response based on intent and data."""

        # Static responses
        if intent in STATIC_RESPONSES:
            return random.choice(STATIC_RESPONSES[intent])

        # Product list
        if intent == "product_list":
            if not all_products:
                return "Sorry, I couldn't load the product catalog right now."

            response = "Here's everything we offer at Anchor Customs!\n\n"
            cards = [self.format_product_card(p) for p in all_products]
            response += "\n".join(cards)
            response += "\n\n<em>DM us on Instagram @anchor.customs to place your order!</em>"
            return response

        # Combo query
        if intent == "combo_query":
            if not all_combos:
                return "Sorry, I couldn't find any combos right now."

            response = "Here are our combo deals - great value! \n\n"
            cards = [self.format_product_card(c) for c in all_combos]
            response += "\n".join(cards)
            response += "\n\n<em>Combos save you money! DM us on Instagram to order.</em>"
            return response

        # Price query
        if intent == "price_query" and search_results:
            if price_filters.get('sort') == 'price_asc':
                cheapest = search_results[0][0]
                response = f"Our most affordable product is **{cheapest['name']}** at just &#8377;{cheapest['price']:,}!\n\n"
                response += self.format_product_card(cheapest)
                return response

            if price_filters.get('sort') == 'price_desc':
                expensive = search_results[0][0]
                response = f"Our premium product is **{expensive['name']}** at &#8377;{expensive['price']:,}!\n\n"
                response += self.format_product_card(expensive)
                return response

            max_p = price_filters.get('max_price', '')
            min_p = price_filters.get('min_price', '')

            if max_p and min_p:
                response = f"Products between &#8377;{min_p:,} and &#8377;{max_p:,}:\n\n"
            elif max_p:
                response = f"Products under &#8377;{max_p:,}:\n\n"
            elif min_p:
                response = f"Products above &#8377;{min_p:,}:\n\n"
            else:
                response = "Here are the matching products:\n\n"

            cards = [self.format_product_card(item) for item, score in search_results]
            response += "\n".join(cards)
            return response

        if intent == "price_query" and not search_results:
            if price_filters and price_filters.get('max_price'):
                return f"Sorry, we don't have any products under &#8377;{price_filters['max_price']:,}. Our most affordable item is **Customised Polaroids** at &#8377;499!"
            return "Could you tell me your budget? For example, 'products under 1000' or 'between 500 and 1500'."

        # Product search / product info
        if intent in ("product_search", "product_info") and search_results:
            if len(search_results) == 1 or (search_results[0][1] > 0.7 and search_results[0][1] - search_results[1][1] > 0.15):
                # High confidence single match
                product = search_results[0][0]
                response = f"Here's what I found:\n\n"
                response += self.format_product_card(product)
                response += "\n\n<em>Want to order? DM us on Instagram @anchor.customs!</em>"
                return response
            else:
                response = "Here are the best matches:\n\n"
                cards = [self.format_product_card(item) for item, score in search_results[:5]]
                response += "\n".join(cards)
                response += "\n\n<em>Want details on any specific product? Just ask!</em>"
                return response

        if intent in ("product_search", "product_info") and not search_results:
            return "I couldn't find products matching your query. Try asking about frames, magazines, scrapbooks, combos, or hampers!"

        # Fallback
        return "I'm not sure I understand. You can ask me about:\n- Our **products** and **prices**\n- **Combo deals**\n- **How to order**\n- Specific items like frames, magazines, scrapbooks, etc."
