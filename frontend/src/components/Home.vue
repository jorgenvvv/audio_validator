<template>
  <v-container>
     <v-overlay :value="loading">
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </v-overlay>

    <v-card v-if="!storeState.isAuthenticated">
      <v-card-title>
        Please log in to continue...
      </v-card-title>
      <v-card-text>
        <v-btn
          @click="authenticate('google')"
          width="210px"
          height="auto"
          class="pa-1"
        >
          <v-avatar size="30" class="mr-2">
            <img
              :src="publicPath + 'assets/google_logo.png'"
            />
          </v-avatar>
          Login With Google
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>
<script>
import axios from 'axios';
import { store } from '../store.js';

export default {
  data() {
    return {
      publicPath: process.env.BASE_URL,
      storeState: store.state,
      loading: false
    };
  },

  created() {
    if (this.$auth.isAuthenticated()) {
      this.$router.push('languages');
    }
  },

  methods: {
    authenticate(provider) {
      if (this.$auth.isAuthenticated()) {
        this.$auth.logout();
      }

      this.loading = true;

      this.$auth
        .authenticate(provider)
        .then(() => {
          store.setAuthenticated(true);
          axios.get(process.env.VUE_APP_API_URL + '/user').then((response) => {
            store.setUserInfo(response.data);
            this.loading = false;
            this.$router.push('languages');
          });
        })
        .catch(error => {
          console.log('Authentication failed', error);
          this.loading = false;
        });
    }
  }
};
</script>
