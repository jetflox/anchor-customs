"""
Training Script for Anchor Customs Chatbot.

This script:
1. Downloads the sentence-transformer model (first time only)
2. Pre-computes embeddings for all products
3. Pre-computes embeddings for all intent examples
4. Validates everything works

Run this once before starting the chatbot server.
"""

import json
import os
import time
from sentence_transformers import SentenceTransformer
from chatbot.intent_classifier import IntentClassifier
from chatbot.product_search import ProductSearchEngine


def main():
    print("=" * 55)
    print("  Anchor Customs Chatbot - Model Training")
    print("=" * 55)
    print()

    # Step 1: Download/Load model
    print("[1/4] Loading sentence-transformer model...")
    print("       (First time downloads ~80MB - needs internet)")
    start = time.time()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    elapsed = time.time() - start
    print(f"       Model loaded in {elapsed:.1f}s")
    print()

    # Step 2: Train intent classifier
    print("[2/4] Training intent classifier...")
    start = time.time()
    classifier = IntentClassifier(model)
    elapsed = time.time() - start
    print(f"       Intent classifier ready in {elapsed:.1f}s")
    print()

    # Step 3: Build product search index
    print("[3/4] Building product search index...")
    start = time.time()
    search_engine = ProductSearchEngine(model)
    elapsed = time.time() - start
    print(f"       Search index built in {elapsed:.1f}s")
    print()

    # Step 4: Run test queries
    print("[4/4] Running test queries...")
    print()

    test_queries = [
        "hi",
        "what can I buy under 500",
        "show me frames",
        "do you have combos",
        "tell me about the magazine",
        "gift for my girlfriend",
        "cheapest product",
        "bye",
    ]

    for query in test_queries:
        intent, confidence = classifier.classify(query)
        price_filters = classifier.extract_price_filter(query)

        print(f'  "{query}"')
        print(f'    -> Intent: {intent} (confidence: {confidence:.3f})')

        if price_filters:
            print(f'    -> Price filters: {price_filters}')

        if intent in ("product_search", "product_info"):
            results = search_engine.search(query, top_k=3)
            if results:
                top_match = results[0][0]['name']
                print(f'    -> Top match: {top_match} (score: {results[0][1]:.3f})')

        elif intent == "price_query" and price_filters:
            results = search_engine.search(query, top_k=3, price_filters=price_filters)
            if results:
                names = [r[0]['name'] for r in results]
                print(f'    -> Found: {", ".join(names)}')
            else:
                print(f'    -> No products in this range')
        print()

    print("=" * 55)
    print("  Training complete! You can now run: python app.py")
    print("=" * 55)


if __name__ == '__main__':
    main()
