export const store = {
  state: {
    isAuthenticated: false
  },

  setAuthenticated(value) {
    this.state.isAuthenticated = value;
  }
};
