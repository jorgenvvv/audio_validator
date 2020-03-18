<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="results"
      :items-per-page="100"
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
        { text: 'Total validated', value: 'total' },
        { text: 'Validation results overlap', value: 'overlap' },
        { text: 'Is given language', value: 'GIVEN_LANG' },
        { text: 'Not given language', value: 'NOT_GIVEN_LANG' },
        { text: 'No speech', value: 'NO_SPEECH' },
        { text: "Don't know", value: 'DO_NOT_KNOW' }
      ]
    };
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/results').then(response => {
      this.results = response.data;
      const fields = ['GIVEN_LANG', 'NOT_GIVEN_LANG', 'NO_SPEECH', 'DO_NOT_KNOW'];
      this.results.map(result => {
        fields.forEach(field => {
          if (!result[field]) result[field] = 0;
        });

        result.language = result.language.name;
        
        const total = result.GIVEN_LANG + result.NOT_GIVEN_LANG + result.NO_SPEECH + result.DO_NOT_KNOW;
        result.total = total;
        result.GIVEN_LANG = (result.GIVEN_LANG / total * 100).toFixed(1) + '%';
        result.NOT_GIVEN_LANG = (result.NOT_GIVEN_LANG / total * 100).toFixed(1) + '%';
        result.NO_SPEECH = (result.NO_SPEECH / total * 100).toFixed(1) + '%';
        result.DO_NOT_KNOW = (result.DO_NOT_KNOW / total * 100).toFixed(1) + '%';

        result.overlap = '-';
        if ('total_validated_twice' in result && 'answer_overlap' in result) {
          result.overlap = (result.answer_overlap / result.total_validated_twice * 100).toFixed(1) + '%';
        }
      });
    });
  }
};
</script>
