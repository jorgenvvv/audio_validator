<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <router-link to="/">
          <span>Audio validator</span>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span class="mr-3" v-if="$route.params.lang">Language: {{ $route.params.lang }}</span>
      <v-btn v-if="$route.name === 'audiovalidator'" to="/" small>Change language</v-btn>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => ({}),
};
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
