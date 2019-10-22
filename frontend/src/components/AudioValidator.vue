<template>
  <v-container>
    <v-alert v-if="audioFiles.length === 0" border="top" colored-border type="info" elevation="2">
      There is no more audio to validate for current language.
    </v-alert>
    <v-card class="pa-2" v-if="audioFiles.length > 0">
      <v-alert v-if="invalidFields" dense outlined type="error">
        A spoken language has to be chosen for all audio clips.
      </v-alert>

      <v-row v-for="file of audioFiles" :key="file.file_name">
        <v-col cols="4">
          <p>{{ file.file_name }}</p>
          <audio controls>
            <source
              :src="
                `${$API_URL}/audio/${$route.params.lang}/${encodeURIComponent(
                  file.file_name
                )}`
              "
            />
            Your browser does not support the audio element.
          </audio>
        </v-col>
        <v-col cols="8">
          <v-row>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="en"
              multiple
              label="English"
            ></v-checkbox>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="fr"
              multiple
              label="French"
            ></v-checkbox>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="ge"
              multiple
              label="German"
            ></v-checkbox>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="et"
              multiple
              label="Estonian"
            ></v-checkbox>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="ru"
              multiple
              label="Russian"
            ></v-checkbox>
            <v-checkbox
              class="mx-2"
              v-model="file.languages"
              value="other"
              multiple
              label="Other"
            ></v-checkbox>
          </v-row>
        </v-col>
      </v-row>
      <div class="d-flex flex-row-reverse">
        <v-btn color="primary" @click="saveValidatedAudio()">Save</v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      audioFiles: [],
      invalidFields: false
    };
  },

  created() {
    this.loadAudio();
  },

  methods: {
    loadAudio() {
      axios
        .get(
          process.env.VUE_APP_API_URL +
            '/audio/' +
            this.$route.params.lang +
            '/all'
        )
        .then(response => {
          this.audioFiles = response.data.filter(
            f => !f.file_name.endsWith('info.json')
          );
        });
    },

    validateAnswers() {
      this.invalidFields = false;

      let allValid = true;
      this.audioFiles = this.audioFiles.map(a => {
        if (!a.hasOwnProperty('languages') || a.languages.length === 0) {
          allValid = false;
          a.valid = false;
        }

        return a;
      });

      this.invalidFields = true;

      return allValid;
    },

    saveValidatedAudio() {
      if (this.validateAnswers()) {
        axios
          .post(process.env.VUE_APP_API_URL + '/audio/validated', {
            lang: this.$route.params.lang,
            data: this.audioFiles
          })
          .then(() => {
            this.invalidFields = false;
            this.loadAudio();
            window.scrollTo(0, 0);
          });
      } else {
        window.scrollTo(0, 0);
      }
    }
  }
};
</script>
