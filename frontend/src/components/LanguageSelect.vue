<template>
  <v-container>
    <v-list>
      <v-list-item-group color="primary">
        <v-list-item v-for="lang in availableLanguages" :key="lang.code" @click="chooseLanguage(lang.code)">
          <v-list-item-content>
            <v-list-item-title>{{ lang.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      availableLanguages: []
    }
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/languages/all')
      .then(response => {
        this.availableLanguages = response.data;
      });
  },

  methods: {
    chooseLanguage(code) {
      this.$router.push(`${code}/validate`);
    }
  }
};
</script>
