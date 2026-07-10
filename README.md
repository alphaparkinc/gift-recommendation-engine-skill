# genpark-gift-recommendation-engine-skill

> **GenPark AI Agent Skill** -- Generate personalized gift recommendations based on recipient profile, budget, occasion, and interests.

## Features

- Interest-to-category mapping (fitness, beauty, tech, travel, cooking, and more)
- Occasion-aware scoring: birthday, wedding, graduation, anniversary, holiday
- Budget fit optimization (ideal: 70-90% of budget)
- Personalized gift messages per occasion
- Wrapping style suggestions
- Ranks all catalog products by match score

## Quick Start

```python
from client import GiftRecommendationClient

client = GiftRecommendationClient()
result = client.recommend(
    recipient={"age": 28, "gender": "female", "interests": ["fitness", "wellness"]},
    occasion="birthday",
    budget_usd=80.0,
    product_catalog=[{"id":"P1","name":"Yoga Mat","price":65,"category":"fitness","tags":["wellness"]}],
)
for rec in result["recommendations"]:
    print(f"{rec['product_name']} -- Score: {rec['match_score']}")
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
