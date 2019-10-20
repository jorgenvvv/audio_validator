<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Audio validator</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
      <AudioValidator/>
    </v-content>
  </v-app>
</template>

<script>
import AudioValidator from './components/AudioValidator';

export default {
  name: 'App',
  components: {
    AudioValidator,
  },
  data: () => ({
    //
  }),
};
</script>
