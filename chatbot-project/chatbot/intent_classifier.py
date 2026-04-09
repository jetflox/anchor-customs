"""
Intent Classifier using Sentence Transformers.
Classifies user messages into predefined intents using cosine similarity.
"""

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .training_data import INTENT_EXAMPLES


class IntentClassifier:
    def __init__(self, model):
        """Initialize with a pre-loaded sentence transformer model."""
        self.model = model
        self.intent_embeddings = {}
        self.intent_labels = []
        self.all_embeddings = None
        self._train()

    def _train(self):
        """Pre-compute embeddings for all intent examples."""
        all_sentences = []
        labels = []

        for intent, examples in INTENT_EXAMPLES.items():
            for example in examples:
                all_sentences.append(example.lower())
                labels.append(intent)

        self.intent_labels = labels
        self.all_embeddings = self.model.encode(all_sentences)
        print(f"Intent classifier trained with {len(all_sentences)} examples across {len(INTENT_EXAMPLES)} intents.")

    def classify(self, text):
        """
        Classify the intent of a given text.
        Returns (intent_name, confidence_score).
        """
        text_lower = text.lower().strip()

        # Encode the input text
        text_embedding = self.model.encode([text_lower])

        # Compute cosine similarity with all training examples
        similarities = cosine_similarity(text_embedding, self.all_embeddings)[0]

        # Find best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        best_intent = self.intent_labels[best_idx]

        # Also compute average score per intent for better classification
        intent_scores = {}
        for i, label in enumerate(self.intent_labels):
            if label not in intent_scores:
                intent_scores[label] = []
            intent_scores[label].append(similarities[i])

        # Use top-3 average per intent
        intent_avg_scores = {}
        for intent, scores in intent_scores.items():
            top_scores = sorted(scores, reverse=True)[:3]
            intent_avg_scores[intent] = np.mean(top_scores)

        best_avg_intent = max(intent_avg_scores, key=intent_avg_scores.get)
        best_avg_score = intent_avg_scores[best_avg_intent]

        # If confidence is too low, default to product_search
        if best_avg_score < 0.3:
            return "product_search", best_avg_score

        return best_avg_intent, best_avg_score

    def extract_price_filter(self, text):
        """
        Extract price constraints from the query.
        Returns dict with 'min_price' and/or 'max_price'.
        """
        text_lower = text.lower()
        filters = {}

        # "under X", "below X", "less than X"
        match = re.search(r'(?:under|below|less than|within|upto|up to|under rs\.?|under ₹)\s*(\d+)', text_lower)
        if match:
            filters['max_price'] = int(match.group(1))

        # "above X", "over X", "more than X"
        match = re.search(r'(?:above|over|more than|greater than|starting from)\s*(\d+)', text_lower)
        if match:
            filters['min_price'] = int(match.group(1))

        # "between X and Y"
        match = re.search(r'between\s*(\d+)\s*(?:and|to|-)\s*(\d+)', text_lower)
        if match:
            filters['min_price'] = int(match.group(1))
            filters['max_price'] = int(match.group(2))

        # "for X rupees" or "X rs"
        if not filters:
            match = re.search(r'(?:for|at)\s*(?:rs\.?|₹)?\s*(\d+)', text_lower)
            if match:
                price = int(match.group(1))
                filters['max_price'] = price

        # "cheapest" or "lowest price"
        if any(word in text_lower for word in ['cheapest', 'lowest price', 'least expensive', 'most affordable']):
            filters['sort'] = 'price_asc'

        # "most expensive" or "highest price"
        if any(word in text_lower for word in ['most expensive', 'highest price', 'premium', 'costliest']):
            filters['sort'] = 'price_desc'

        return filters
