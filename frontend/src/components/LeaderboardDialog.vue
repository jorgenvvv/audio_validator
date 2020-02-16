<template>
  <v-dialog v-model="storeState.leaderboardDialogVisibility" width="600">
    <v-card>
      <v-card-title class="headline">
        Leaderboard
      </v-card-title>
      <v-divider class="mb-3"></v-divider>
      <v-card-text class="text--primary text-center">
        <v-list-item v-for="row in leaderboard" :key="row.created_by">
          <v-list-item-content>
            <v-list-item-title v-if="storeState.userInfo.email === row.created_by" class="font-weight-bold">
              {{ formatUserRank(row.user_rank) }}. {{ storeState.userInfo.name }} ({{ row.cnt }})
            </v-list-item-title>
            <v-list-item-title v-else>
              {{ formatUserRank(row.user_rank) }}. USER_{{ row.created_by }} ({{ row.cnt }})
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="closeLeaderboardDialog()">
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { store } from '../store.js';
import { EventBus } from '../event-bus.js';

import axios from 'axios';

export default {
  name: 'leaderboard-dialog',

  data() {
    return {
      storeState: store.state,
      leaderboard: []
    };
  },

  created() {
    this.loadLeaderboardData();

    EventBus.$on('update-leaderboard', () => {
      this.loadLeaderboardData();
      console.log('leader update')
    });
  },

  methods: {
    loadLeaderboardData() {
      axios
        .get(process.env.VUE_APP_API_URL + '/user/leaderboard')
        .then(response => {
          this.leaderboard = response.data;
        });
    },

    closeLeaderboardDialog() {
      store.setLeaderboardDialogVisibility(false);
    },

    formatUserRank(rank) {
      if (rank === 1)
        return '🥇 ' + rank;
      else if (rank === 2)
        return '🥈 ' + rank;
      else if (rank === 3)
        return '🥉 ' + rank;
      else 
        return rank;
    }
  }
};
</script>