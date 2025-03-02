const { ApolloServer } = require("@apollo/server");
const { startStandaloneServer } = require("@apollo/server/standalone");

const typeDefs = require("./schema");
const resolvers = require("./resolvers");

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => { // ✅ FIX: Use `req`
    if (!req) {
      console.log("❌ Request is undefined!");
      throw new Error("Request object is missing in context!");
    }

    // console.log("🔍 Headers:", req.headers);
    const token = req.headers.authorization || ""; // ✅ FIX: Properly access headers
    // console.log("🔑 Received Token:", token);
    return { token };
  },
}).then(({ url }) => {
  console.log(`🚀 GraphQL Gateway running at ${url}`);
});
