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
      <v-menu left bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-settings</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/">
            <v-list-item-title>Change language</v-list-item-title>
          </v-list-item>
          <v-list-item @click="dialog = true">
            <v-list-item-title>Change name</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
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
                <v-text-field v-model="userName" label="Name" required></v-text-field>
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
export default {
  name: 'App',
  data() {
    return {
      dialog: false,
      userName: null
    }
  },

  created() {
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
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
