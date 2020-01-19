<template>
  <v-app>
    <v-app-bar app dense>
      <v-toolbar-title class="headline text-uppercase">
        <router-link to="/">
          <span>Audio validator</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span class="mr-3" v-if="$route.params.lang">
        Language: {{ $route.params.lang }}
      </span>
      <span class="mr-3" v-if="storeState.isAuthenticated">
        <v-btn @click="logout()">Logout</v-btn>
      </span>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>

    <v-row v-if="dialog" justify="center">
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Change your name</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-text-field
                  v-model="userName"
                  label="Name"
                  required
                ></v-text-field>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="dialog = false">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="saveName()">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-app>
</template>

<script>
import { store } from './store.js';

export default {
  name: 'App',
  data() {
    return {
      dialog: false,
      userName: null,
      storeState: store.state
    };
  },

  created() {
    store.setAuthenticated(this.$auth.isAuthenticated());

    if (sessionStorage.getItem('userName')) {
      this.userName = sessionStorage.getItem('userName');
    }
  },

  methods: {
    saveName() {
      if (this.userName) {
        sessionStorage.setItem('userName', this.userName);
        this.dialog = false;
      }
    },

    logout() {
      this.$auth.logout().then(() => {
        store.setAuthenticated(false);
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
