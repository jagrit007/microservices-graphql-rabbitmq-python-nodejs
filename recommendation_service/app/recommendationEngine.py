import random

# Mock data for user purchase and browsing history
USER_PURCHASE_HISTORY = {
    1: ["product_1", "product_2"],
    2: ["product_3", "product_4"],
    3: ["product_2", "product_5"]
}

SIMILAR_PRODUCTS = {
    "product_1": ["product_6", "product_7"],
    "product_2": ["product_8", "product_9"],
    "product_3": ["product_10", "product_11"],
    "product_4": ["product_12", "product_13"],
    "product_5": ["product_14", "product_15"]
}


async def generate_recommendations(user_id: int) -> list:
    """
    Generates simple recommendations based on user purchase history.
    """
    purchased = USER_PURCHASE_HISTORY.get(user_id, [])
    recommendations = []

    for product in purchased:
        recommendations.extend(SIMILAR_PRODUCTS.get(product, []))

    return random.sample(recommendations, min(len(recommendations), 3))  # Return up to 3 recommendations
