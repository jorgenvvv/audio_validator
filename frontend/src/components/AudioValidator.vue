<template>
  <v-container>
    <v-row v-for="file of audioFiles" :key="file">
      <v-col cols="4">
        <p>{{file}}</p>
        <audio controls>
          <source :src="$API_URL + '/audio/' + encodeURIComponent(file)">
          Your browser does not support the audio element.
        </audio>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      audioFiles: []
    }
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/audio/all')
      .then(response => {
        this.audioFiles = response.data.filter(f => !f.endsWith('info.json'));
      })
  }
};
</script>
