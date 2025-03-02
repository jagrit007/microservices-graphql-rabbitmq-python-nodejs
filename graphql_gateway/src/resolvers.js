const { GraphQLScalarType, Kind } = require("graphql");
const { getUser } = require("./services/userService");
const { getNotifications } = require("./services/notificationService");
const { getRecommendations } = require("./services/recommendationService");

const resolvers = {
  JSON: new GraphQLScalarType({
    name: "JSON",
    description: "Arbitrary JSON values",
    serialize(value) {
      return value; // Return JSON as is
    },
    parseValue(value) {
      return value; // Accept JSON input
    },
    parseLiteral(ast) {
      if (ast.kind === Kind.OBJECT) {
        return ast.value;
      }
      return null;
    }
  }),

  Query: {
    user: async (_, { id }, { token }) => {
      return await getUser(id, token);
    },

    notifications: async (_, { userId }, { token }) => {
      return getNotifications(userId, token);
    },

    recommendations: async (_, { userId }, { token }) => {
      return await getRecommendations(userId, token);
    },
  },
};

module.exports = resolvers;
