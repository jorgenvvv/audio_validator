export const store = {
  state: {
    isAuthenticated: false,
    userInfo: {},
    helpModalVisibility: false,
    leaderboardDialogVisibility: false
  },

  setAuthenticated(value) {
    this.state.isAuthenticated = value;
  },

  setUserInfo(value) {
    this.state.userInfo = value;
  },

  setHelpModalVisibility(value) {
    this.state.helpModalVisibility = value;
  },

  setLeaderboardDialogVisibility(value) {
    this.state.leaderboardDialogVisibility = value;
  }

};
