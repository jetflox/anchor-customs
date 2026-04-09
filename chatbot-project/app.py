"""
Anchor Customs Chatbot - Flask Application
Main entry point for the chatbot server.
"""

from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from chatbot.intent_classifier import IntentClassifier
from chatbot.product_search import ProductSearchEngine
from chatbot.response_generator import ResponseGenerator

app = Flask(__name__)

# ── Load AI Model ──────────────────────────────────────────────
print("Loading AI model (first time downloads ~80MB)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")

# ── Initialize Components ─────────────────────────────────────
intent_classifier = IntentClassifier(model)
search_engine = ProductSearchEngine(model)
response_generator = ResponseGenerator()


@app.route('/')
def home():
    """Serve the chat UI."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'response': 'Please type a message!'})

    # Step 1: Classify intent
    intent, confidence = intent_classifier.classify(user_message)
    print(f"Intent: {intent} (confidence: {confidence:.3f})")

    # Step 2: Extract price filters if present
    price_filters = intent_classifier.extract_price_filter(user_message)
    if price_filters:
        intent = "price_query"

    # Step 3: Search products if needed
    search_results = None
    all_products = None
    all_combos = None

    if intent in ("product_search", "product_info"):
        search_results = search_engine.search(user_message, top_k=5)

    elif intent == "price_query":
        search_results = search_engine.search(
            user_message,
            top_k=10,
            price_filters=price_filters
        )

    elif intent == "product_list":
        all_products = search_engine.get_all_products()

    elif intent == "combo_query":
        all_combos = search_engine.get_all_combos()

    # Step 4: Generate response
    response = response_generator.generate(
        intent=intent,
        search_results=search_results,
        price_filters=price_filters,
        all_products=all_products,
        all_combos=all_combos,
    )

    return jsonify({
        'response': response,
        'intent': intent,
        'confidence': round(confidence, 3),
    })


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Anchor Customs Chatbot is running!")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
