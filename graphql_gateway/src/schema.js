const { gql } = require("apollo-server");

const typeDefs = gql`
  scalar JSON

  type User {
    id: ID!
    name: String!
    email: String!
    preferences: [String!]
  }

  type Notification {
    id: ID!
    userId: ID!
    type: String!
    content: JSON!  # Change from String to JSON
    sentAt: String!
    read: Boolean!
  }

  type Recommendation {
    id: ID!
    userId: ID!
    products: [String!]!
  }

  type Query {
    user(id: ID!): User
    notifications(userId: ID!): [Notification!]
    recommendations(userId: ID!): Recommendation
  }
`;

module.exports = typeDefs;
