"""
example_usage.py -- Demonstrates the GiftRecommendationClient SDK.
"""
from client import GiftRecommendationClient

def main():
    client = GiftRecommendationClient()

    catalog = [
        {"id": "P01", "name": "Vitamin C Serum Set", "price": 45.00, "category": "beauty", "tags": ["skincare", "personal", "lifestyle"]},
        {"id": "P02", "name": "Yoga Mat Premium", "price": 68.00, "category": "fitness", "tags": ["wellness", "yoga", "experience"]},
        {"id": "P03", "name": "Wireless Earbuds Pro", "price": 89.00, "category": "electronics", "tags": ["tech", "gadgets", "lifestyle"]},
        {"id": "P04", "name": "Scented Candle Gift Set", "price": 38.00, "category": "home", "tags": ["cozy", "aromatherapy", "personal"]},
        {"id": "P05", "name": "Running Shoes", "price": 120.00, "category": "fitness", "tags": ["sports", "fitness", "activewear"]},
        {"id": "P06", "name": "Travel Skincare Kit", "price": 55.00, "category": "beauty", "tags": ["travel", "skincare", "personal"]},
        {"id": "P07", "name": "Smart Water Bottle", "price": 42.00, "category": "fitness", "tags": ["wellness", "tech", "practical"]},
        {"id": "P08", "name": "Gourmet Coffee Sampler", "price": 35.00, "category": "food", "tags": ["cooking", "gourmet", "lifestyle"]},
    ]

    print("[Gift Recommendation Engine]")
    result = client.recommend(
        recipient={"age": 28, "gender": "female", "interests": ["fitness", "beauty", "wellness"], "relationship": "friend"},
        occasion="birthday",
        budget_usd=80.00,
        product_catalog=catalog,
        top_n=4,
    )

    print(f"Occasion: {result['occasion']} | Recipient: {result['recipient_summary']}")
    print(f"Budget: ${result['budget_usd']} | Products Evaluated: {result['total_products_evaluated']}")
    print(f"\nTop {len(result['recommendations'])} Recommendations:")
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"  {i}. {rec['product_name']} -- ${rec['price']} ({rec['budget_fit']})")
        print(f"     Score: {rec['match_score']} | Reasons: {'; '.join(rec['match_reasons'])}")
    print(f"\nGift Message: {result['gift_message']}")
    print(f"Wrapping: {result['gift_wrapping_suggestion']}")

if __name__ == "__main__":
    main()
