<template>
  <v-app>
    <v-app-bar app dense>
      <v-toolbar-title class="headline text-uppercase">
        <router-link to="/">
          <span>Audio validator</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span class="mr-3 text-uppercase" v-if="$route.params.lang">
        <v-icon>mdi-web</v-icon>
        {{ $route.params.lang }}
      </span>
      <span class="mr-3" v-if="storeState.isAuthenticated">
        <v-icon>mdi-account-circle-outline</v-icon>
        {{ storeState.userInfo.name }}
      </span>
      <span class="mr-3" v-if="storeState.isAuthenticated">
        <v-btn depressed small @click="logout()">
          Logout
        </v-btn>
      </span>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios';
import { store } from './store.js';

export default {
  name: 'App',
  data() {
    return {
      dialog: false,
      storeState: store.state
    };
  },

  created() {
    store.setAuthenticated(this.$auth.isAuthenticated());

    if (this.storeState.isAuthenticated) {
      axios.get(process.env.VUE_APP_API_URL + '/user').then((response) => {
        store.setUserInfo(response.data);
      });
    }
  },

  methods: {
    logout() {
      this.$auth.logout().then(() => {
        store.setAuthenticated(false);
        store.setUserInfo({});
        this.$router.push('/');
      });
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
