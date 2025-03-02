const axios = require("axios");
const RECOMMENDATION_SERVICE_URL = process.env.RECOMMENDATION_SERVICE_URL;

async function getRecommendations(userId, token) {
  try {
    const response = await axios.get(`${RECOMMENDATION_SERVICE_URL}/recommendations/${userId}`, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    });

    if (!response.data) return null;

    // Transform response to match GraphQL schema
    const recommendation = {
      id: response.data._id,  // Convert MongoDB _id to id
      userId: response.data.user_id, // Convert snake_case to camelCase
      products: response.data.products,
    };

    return recommendation;
  } catch (error) {
    console.error("Error fetching recommendations:", error.message);
    return null;
  }
}

module.exports = { getRecommendations };
