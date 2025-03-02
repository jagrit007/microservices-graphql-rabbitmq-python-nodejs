const axios = require("axios");
const USER_SERVICE_URL = process.env.USER_SERVICE_URL;

async function getUser(id, token) {
  try {
    const response = await axios.get(`${USER_SERVICE_URL}/users/${id}`, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user:", error.message);
    return null;
  }
}

module.exports = { getUser };
