<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="results"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
  </v-container>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      results: [],
      headers: [
        { text: 'Language', value: 'language' },
        { text: 'Is Given Language', value: 'GIVEN_LANG' },
        { text: 'Not Given Language', value: 'NOT_GIVEN_LANG' },
        { text: 'No Speech  ', value: 'NO_SPEECH' }
      ]
    };
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/results').then(response => {
      this.results = response.data;
      this.results.map(result => {
        const total = result.GIVEN_LANG + result.NOT_GIVEN_LANG + result.NO_SPEECH;
        result.GIVEN_LANG = (result.GIVEN_LANG / total * 100).toFixed(1) + '%';
        result.NOT_GIVEN_LANG = (result.NOT_GIVEN_LANG / total * 100).toFixed(1) + '%';
        result.NO_SPEECH = (result.NO_SPEECH / total * 100).toFixed(1) + '%';
      });
    });
  }
};
</script>
