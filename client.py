"""
gift-recommendation-engine-skill: Client SDK
Generate personalized gift recommendations for e-commerce occasions.
"""
from __future__ import annotations
from typing import Optional

OCCASION_WEIGHTS = {
    "birthday":    {"experience": 0.3, "personal": 0.4, "practical": 0.3},
    "wedding":     {"experience": 0.2, "personal": 0.2, "practical": 0.6},
    "holiday":     {"experience": 0.2, "personal": 0.3, "practical": 0.5},
    "graduation":  {"experience": 0.4, "personal": 0.3, "practical": 0.3},
    "anniversary": {"experience": 0.5, "personal": 0.4, "practical": 0.1},
    "default":     {"experience": 0.3, "personal": 0.3, "practical": 0.4},
}

INTEREST_CATEGORY_MAP = {
    "fitness":    ["sports", "fitness", "health", "wellness", "activewear"],
    "beauty":     ["beauty", "skincare", "cosmetics", "personal care"],
    "travel":     ["travel", "luggage", "accessories", "outdoor"],
    "tech":       ["electronics", "gadgets", "tech", "smart home"],
    "cooking":    ["kitchen", "food", "cooking", "gourmet"],
    "reading":    ["books", "stationery", "education"],
    "gaming":     ["gaming", "electronics", "entertainment"],
    "fashion":    ["clothing", "accessories", "fashion", "jewelry"],
    "home":       ["home", "decor", "furniture", "kitchen"],
    "wellness":   ["wellness", "health", "aromatherapy", "yoga"],
}

GIFT_MESSAGES = {
    "birthday": [
        "Wishing you a wonderful birthday! Hope this brings a smile to your face.",
        "Happy Birthday! Here is something special just for you.",
        "Celebrating you today and every day. Enjoy your special gift!",
    ],
    "wedding": [
        "Congratulations on your special day! Wishing you a lifetime of happiness.",
        "Here is to love, laughter, and happily ever after. Congratulations!",
        "A small token of love as you begin your new chapter together.",
    ],
    "holiday": [
        "Season's greetings! Wishing you joy and warmth this holiday season.",
        "Happy Holidays! Hope this gift adds a little extra magic to your season.",
        "With warmth and best wishes for a wonderful holiday season.",
    ],
    "graduation": [
        "Congratulations Graduate! The world is yours -- go get it!",
        "So proud of everything you have achieved. Here is to your next adventure!",
        "Your hard work paid off. Congratulations on this amazing milestone!",
    ],
    "anniversary": [
        "Celebrating another year of love and memories together.",
        "Happy Anniversary! Here is to many more years of joy and togetherness.",
        "Every year with you is a gift. Happy Anniversary!",
    ],
    "default": [
        "Thinking of you! Hope this brightens your day.",
        "A little something special, just for you.",
    ],
}

WRAPPING_STYLES = {
    "birthday":    "Bright, colorful wrapping with ribbon and a gift tag. Add confetti for extra fun!",
    "wedding":     "Elegant white or ivory wrapping with satin ribbon and a wax-sealed card.",
    "holiday":     "Classic red-and-green or winter-themed paper with a festive bow.",
    "graduation":  "School colors if known, or bright gold/silver. Add a small graduation charm.",
    "anniversary": "Romantic deep red or rose gold wrapping with a personal handwritten note.",
    "default":     "Clean kraft paper with a simple ribbon and personal message card.",
}


class GiftRecommendationClient:
    """
    SDK for generating personalized gift recommendations.
    Scores products based on recipient interests, occasion, and budget fit.
    """

    def recommend(
        self,
        recipient: dict,
        occasion: str,
        budget_usd: float,
        product_catalog: list[dict],
        top_n: int = 5,
    ) -> dict:
        """
        Generate gift recommendations.

        Args:
            recipient:       Profile with: age (int), gender (str), interests (list[str]), relationship (str).
            occasion:        Gift occasion string.
            budget_usd:      Maximum gift budget.
            product_catalog: List of {id, name, price, category, tags}.
            top_n:           Number of recommendations to return.

        Returns:
            dict with recommendations, gift_message, gift_wrapping_suggestion
        """
        occasion_key = occasion.lower()
        interests = [i.lower() for i in recipient.get("interests", [])]
        age = int(recipient.get("age", 30))
        gender = str(recipient.get("gender", "any")).lower()

        # Build interest -> category mapping
        interest_categories = set()
        for interest in interests:
            for key, cats in INTEREST_CATEGORY_MAP.items():
                if interest in key or key in interest:
                    interest_categories.update(cats)

        scored = []
        for product in product_catalog:
            price = float(product.get("price", 0))
            if price > budget_usd or price <= 0:
                continue

            score, reasons = self._score_product(
                product, price, budget_usd, interest_categories,
                interests, occasion_key, age, gender
            )
            if score > 0:
                scored.append({
                    "product_id": product.get("id", ""),
                    "product_name": product.get("name", ""),
                    "price": price,
                    "match_score": round(score, 2),
                    "match_reasons": reasons,
                    "budget_fit": f"{round(price/budget_usd*100)}% of budget",
                })

        scored.sort(key=lambda x: x["match_score"], reverse=True)
        recommendations = scored[:top_n]

        import random
        msgs = GIFT_MESSAGES.get(occasion_key, GIFT_MESSAGES["default"])
        gift_message = random.choice(msgs)
        wrapping = WRAPPING_STYLES.get(occasion_key, WRAPPING_STYLES["default"])

        return {
            "occasion": occasion,
            "recipient_summary": f"{age}yo {gender}, interests: {', '.join(interests[:3]) or 'general'}",
            "budget_usd": budget_usd,
            "recommendations": recommendations,
            "gift_message": gift_message,
            "gift_wrapping_suggestion": wrapping,
            "total_products_evaluated": len(product_catalog),
        }

    def _score_product(self, product, price, budget, interest_cats, interests, occasion, age, gender):
        score = 0.0
        reasons = []
        cat = str(product.get("category", "")).lower()
        tags = [t.lower() for t in product.get("tags", [])]
        all_text = cat + " " + " ".join(tags)

        # Interest match
        matched_interests = [i for i in interests if i in all_text]
        if matched_interests:
            score += 40 * min(len(matched_interests), 2) / 2
            reasons.append(f"Matches recipient interest: {matched_interests[0]}")

        # Category match
        if any(ic in all_text for ic in interest_cats):
            score += 20
            if not reasons:
                reasons.append("Fits recipient category preference")

        # Budget fit (sweet spot: 70-90% of budget)
        budget_ratio = price / budget
        if 0.70 <= budget_ratio <= 0.95:
            score += 15
            reasons.append("Ideal budget utilization")
        elif 0.50 <= budget_ratio < 0.70:
            score += 8
        elif budget_ratio < 0.3:
            score -= 5  # Too cheap relative to budget

        # Occasion bonus
        occasion_tags = {
            "birthday": ["personal", "fun", "lifestyle", "experience"],
            "wedding": ["home", "kitchen", "decor", "luxury"],
            "graduation": ["tech", "career", "travel", "experience"],
            "anniversary": ["jewelry", "luxury", "romantic", "experience"],
            "holiday": ["cozy", "lifestyle", "family", "seasonal"],
        }
        bonus_tags = occasion_tags.get(occasion, [])
        if any(bt in all_text for bt in bonus_tags):
            score += 10
            reasons.append(f"Great {occasion} gift choice")

        return score, reasons[:2]
