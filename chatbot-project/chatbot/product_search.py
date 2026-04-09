"""
Product Search Engine using Sentence Transformers.
Performs semantic search over products using cosine similarity.
"""

import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class ProductSearchEngine:
    def __init__(self, model):
        """Initialize with a pre-loaded sentence transformer model."""
        self.model = model
        self.products = []
        self.combos = []
        self.all_items = []
        self.item_texts = []
        self.item_embeddings = None
        self._load_products()
        self._build_index()

    def _load_products(self):
        """Load products from JSON file."""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.products = data.get('products', [])
        self.combos = data.get('combos', [])
        self.all_items = self.products + self.combos
        print(f"Loaded {len(self.products)} products and {len(self.combos)} combos.")

    def _build_index(self):
        """Build semantic search index by computing embeddings for all products."""
        self.item_texts = []
        for item in self.all_items:
            # Create a rich text representation for each product
            text_parts = [
                item['name'],
                item.get('description', ''),
                item.get('type', ''),
                f"price {item['price']} rupees",
            ]
            if item.get('badge'):
                text_parts.append(item['badge'])
            if item.get('includes'):
                text_parts.append("includes " + ", ".join(item['includes']))

            # Add category keywords
            name_lower = item['name'].lower()
            if 'frame' in name_lower:
                text_parts.extend(['frame', 'photo frame', 'wall decor', 'gift frame',
                                   'gift for mom', 'gift for mother', 'gift for dad',
                                   'gift for girlfriend', 'gift for boyfriend',
                                   'gift for friend', 'gift for her', 'gift for him',
                                   'birthday gift', 'anniversary gift'])
            if 'magazine' in name_lower:
                text_parts.extend(['magazine', 'photo book', 'memory book', 'photos',
                                   'gift for mom', 'gift for mother', 'gift for parents',
                                   'gift for girlfriend', 'gift for boyfriend',
                                   'gift for best friend', 'gift for wife', 'gift for husband',
                                   'birthday gift', 'anniversary gift', 'valentine gift'])
            if 'mystery' in name_lower and 'her' in name_lower:
                text_parts.extend(['mystery', 'surprise', 'gift box', 'surprise box',
                                   'gift for her', 'gift for girlfriend', 'gift for wife',
                                   'gift for mom', 'gift for mother', 'gift for sister',
                                   'gift for female', 'gift for woman', 'gift for girl',
                                   'birthday gift for her'])
            elif 'mystery' in name_lower and 'him' in name_lower:
                text_parts.extend(['mystery', 'surprise', 'gift box', 'surprise box',
                                   'gift for him', 'gift for boyfriend', 'gift for husband',
                                   'gift for dad', 'gift for father', 'gift for brother',
                                   'gift for male', 'gift for man', 'gift for boy',
                                   'birthday gift for him'])
            if 'hamper' in name_lower:
                text_parts.extend(['hamper', 'gift hamper', 'gift basket', 'collection',
                                   'gift for anyone', 'gift for mom', 'gift for mother',
                                   'gift for girlfriend', 'gift for boyfriend',
                                   'gift for best friend', 'gift for parents',
                                   'birthday gift', 'anniversary gift'])
            if 'combo' in name_lower:
                text_parts.extend(['combo', 'bundle', 'deal', 'package', 'value', 'save'])
            if 'polaroid' in name_lower:
                text_parts.extend(['polaroid', 'photos', 'prints', 'photo prints',
                                   'gift for mom', 'gift for girlfriend', 'gift for friend',
                                   'gift for her', 'gift for him', 'birthday gift'])
            if 'calendar' in name_lower:
                text_parts.extend(['calendar', 'dates', 'months', 'year', 'wall calendar',
                                   'gift for mom', 'gift for mother', 'gift for parents',
                                   'gift for dad', 'gift for father'])
            if 'scrapbook' in name_lower:
                text_parts.extend(['scrapbook', 'memory', 'memories', 'diary', 'journal',
                                   'gift for mom', 'gift for mother', 'gift for girlfriend',
                                   'gift for best friend', 'gift for wife',
                                   'birthday gift', 'anniversary gift'])
            if 'action' in name_lower:
                text_parts.extend(['action figure', 'toy', 'figurine', 'bricks', 'lego',
                                   'gift for him', 'gift for boyfriend', 'gift for boy',
                                   'gift for brother', 'fun gift'])
            if 'song' in name_lower:
                text_parts.extend(['song', 'music', 'spotify', 'playlist',
                                   'gift for girlfriend', 'gift for boyfriend',
                                   'romantic gift', 'valentine gift', 'anniversary gift'])

            # Add gift-related keywords for all products
            text_parts.extend(['gift', 'customised', 'personalised', 'handcrafted'])

            self.item_texts.append(" ".join(text_parts))

        self.item_embeddings = self.model.encode(self.item_texts)
        print(f"Built search index with {len(self.item_texts)} items.")

    def search(self, query, top_k=5, price_filters=None):
        """
        Search for products matching the query.
        Returns list of (product, score) tuples.
        """
        # Filter items by price first if filters are present
        candidate_indices = list(range(len(self.all_items)))

        if price_filters:
            filtered = []
            for i in candidate_indices:
                price = self.all_items[i]['price']
                if 'min_price' in price_filters and price < price_filters['min_price']:
                    continue
                if 'max_price' in price_filters and price > price_filters['max_price']:
                    continue
                filtered.append(i)
            candidate_indices = filtered

        if not candidate_indices:
            return []

        # Encode query
        query_embedding = self.model.encode([query.lower()])

        # Get embeddings for candidates only
        candidate_embeddings = self.item_embeddings[candidate_indices]

        # Compute similarity
        similarities = cosine_similarity(query_embedding, candidate_embeddings)[0]

        # Sort by similarity or price if requested
        results = []
        for idx, sim in zip(candidate_indices, similarities):
            results.append((self.all_items[idx], float(sim)))

        if price_filters and price_filters.get('sort') == 'price_asc':
            results.sort(key=lambda x: x[0]['price'])
        elif price_filters and price_filters.get('sort') == 'price_desc':
            results.sort(key=lambda x: x[0]['price'], reverse=True)
        else:
            results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def get_all_products(self):
        """Return all products sorted by price."""
        return sorted(self.products, key=lambda x: x['price'])

    def get_all_combos(self):
        """Return all combos sorted by price."""
        return sorted(self.combos, key=lambda x: x['price'])

    def get_products_by_price(self, max_price=None, min_price=None):
        """Filter products by price range."""
        results = []
        for item in self.all_items:
            price = item['price']
            if max_price and price > max_price:
                continue
            if min_price and price < min_price:
                continue
            results.append(item)
        return sorted(results, key=lambda x: x['price'])
