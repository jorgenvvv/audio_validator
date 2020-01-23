export const store = {
  state: {
    isAuthenticated: false,
    userInfo: {}
  },

  setAuthenticated(value) {
    this.state.isAuthenticated = value;
  },

  setUserInfo(value) {
    this.state.userInfo = value;
  }
};
