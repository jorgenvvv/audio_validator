<template>
  <v-container>

    <v-card v-if="!storeState.isAuthenticated">
      <v-card-title>
        Please log in to continue...
      </v-card-title>
      <v-card-text>
        <v-btn @click="authenticate('google')" width="210px" height="auto" class="pa-1">
          <v-avatar size="30" class="mr-2">
            <img src="https://www.freepnglogos.com/uploads/google-logo-png/google-logo-png-suite-everything-you-need-know-about-google-newest-0.png">
          </v-avatar>
          Login With Google
        </v-btn>
      </v-card-text>
    </v-card>

    <v-row>
      <div v-if="storeState.isAuthenticated">
        You are successfully authenticated
        <div>{{$auth.getToken()}}</div>
      </div>
      <hr>
    </v-row>

  </v-container>
</template>
<script>
import { store } from "../store.js";

export default {
  data() {
    return {
      storeState: store.state
    }
  },

  created() {
    if (this.$auth.isAuthenticated()) {
      this.$router.push('languages');
    }
  },

  methods: {
    authenticate (provider) {
      if (this.$auth.isAuthenticated()) {
        this.$auth.logout();
      }

      this.$auth.authenticate(provider)
        .then(() => {
          store.setAuthenticated(true);
          this.$router.push('languages');
        }).catch(error => {
          console.log('Authentication failed', error);
        });
    }
  }
};
</script>
