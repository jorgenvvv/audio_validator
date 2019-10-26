<template>
  <v-container>
    <v-list>
      <v-list-item v-for="lang in availableLanguages" :key="lang.code" @click="enterName(lang.code)">
        <v-list-item-content>
          <v-list-item-title>{{ lang.name }} ({{ lang.validated }} / {{ lang.total }})</v-list-item-title>
          <v-list-item-subtitle>
            <v-progress-linear :value="validatedPercentage(lang.total, lang.validated)" height="25">
              <strong>{{ validatedPercentage(lang.total, lang.validated) }}%</strong>
            </v-progress-linear>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>


  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Please enter your name</span>
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
          <v-btn color="blue darken-1" text @click="saveName()">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>

  </v-container>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      availableLanguages: [],
      selectedLanguage: null,
      userName: null,
      dialog: false
    }
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/languages/all')
      .then(response => {
        this.availableLanguages = response.data;
      });
  },

  methods: {
    enterName(languageCode) {
      this.selectedLanguage = languageCode;

      if (sessionStorage.getItem('userName')) {
        this.chooseLanguage();
      }

      this.dialog = true;
    },

    saveName() {
      sessionStorage.setItem('userName', this.userName);
      this.chooseLanguage();
    },

    chooseLanguage() {
      this.$router.push(`${this.selectedLanguage}/validate`);
    },

    validatedPercentage(total, validated) {
      return (validated / total * 100).toFixed(1);
    }
  }
};
</script>
