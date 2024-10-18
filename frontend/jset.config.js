module.exports = {
  transform: {
    "^.+\\.(js|jsx)$": "babel-jest",
  },
  moduleNameMapper: {
    "^axios$": require.resolve("axios"), // Ensure Jest can resolve axios correctly
  },
};
