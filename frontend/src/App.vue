<template>
  <v-app>
    <v-app-bar app dense>
      <v-toolbar-title class="headline text-uppercase d-none d-sm-flex">
        <router-link to="/">
          <span>Audio validator</span>
        </router-link>
      </v-toolbar-title>
      <span class="mr-3 text-uppercase">
        <router-link to="/">
          <v-icon>mdi-home</v-icon>
        </router-link>
      </span>
      <v-spacer></v-spacer>
      <span class="mr-3 text-uppercase">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn text icon v-on="on" @click="openValidationHelpDialog()">
              <v-icon>mdi-help-circle-outline</v-icon>
            </v-btn>
          </template>
          <span>Validation Instructions</span>
        </v-tooltip>
      </span>
      <span class="mr-3 text-uppercase" v-if="$route.params.lang">
        <v-icon>mdi-web</v-icon>
        {{ $route.params.lang }}
      </span>
      <span class="mr-3 d-none d-sm-flex" v-if="storeState.isAuthenticated">
        <v-icon>mdi-account-circle-outline</v-icon>
        {{ storeState.userInfo.name }}
      </span>
      <span class="mr-3" v-if="storeState.isAuthenticated">
        <v-btn depressed small @click="logout()">
          Logout
        </v-btn>
      </span>
    </v-app-bar>

    <validation-help-dialog></validation-help-dialog>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios';
import { store } from './store.js';
import ValidationHelpDialog from './components/ValidationHelpDialog';

export default {
  name: 'App',
  components: {
    ValidationHelpDialog
  },
  data() {
    return {
      dialog: false,
      storeState: store.state
    };
  },

  created() {
    store.setAuthenticated(this.$auth.isAuthenticated());

    if (this.storeState.isAuthenticated) {
      axios.get(process.env.VUE_APP_API_URL + '/user').then(response => {
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
    },

    openValidationHelpDialog() {
      store.setHelpModalVisibility(true);
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
