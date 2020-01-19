<template>
  <v-container>
    <v-alert
      v-if="audioFiles.length === 0 && !loading"
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      There is no more audio to validate for current language.
    </v-alert>
    <v-overlay :value="loading">
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-card class="pa-2" v-if="audioFiles.length > 0">
      <v-alert v-if="invalidFields" dense outlined type="error">
        A spoken language has to be chosen for all audio clips.
      </v-alert>

      <div :class="file.language ? validatedClasses : ''" v-for="file of audioFiles" :key="file.file_name">
        <v-row @keyup.68="selectCurrentLanguageOption(file)" @keyup.78="playNextAudio(file.file_name)">
          <v-col cols="4">
            <v-row class="pl-6 py-1" v-if="file.metadata">
              <v-col class="pa-0">
                <div>{{ file.metadata.title }}</div>
                <div class="caption">Segment: {{ file.file_name | getSegment }}</div>
              </v-col>
            </v-row>
            <v-row class="pl-6">
              <v-row>
                <div>
                  <audio
                    controls
                    :ref="file.file_name"
                    @play="pauseOtherAudios(file.file_name)"
                  >
                    <source
                      :src="
                        `${$API_URL}/audio/${
                          $route.params.lang
                        }/${encodeURIComponent(file.file_name)}`
                      "
                    />
                    Your browser does not support the audio element.
                  </audio>
                </div>
              </v-row>
            </v-row>
          </v-col>
          <v-col cols="8">
            <v-row>
              <v-radio-group v-model="file.language" row>
                <v-radio label="Is Given Language" value="GIVEN_LANG"></v-radio>
                <v-radio label="Not Given Language" value="NOT_GIVEN_LANG"></v-radio>
                <v-radio label="No Speech" value="NO_SPEECH"></v-radio>
              </v-radio-group>
            </v-row>
          </v-col>
        </v-row>
        <v-divider></v-divider>
      </div>
      <div class="d-flex flex-row-reverse">
        <v-btn class="ma-4" color="primary" @click="saveValidatedAudio()">Save</v-btn>
      </div>

      <v-snackbar v-model="snackbar" :timeout="3000" color="success">
        Saved successfully.
        <v-btn dark text @click="snackbar = false">
          Close
        </v-btn>
      </v-snackbar>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      validationLanguageOptions: [],
      audioFiles: [],
      invalidFields: false,
      snackbar: false,
      loading: false
    };
  },

  created() {
    this.loading = true;
    axios.all([
      this.loadValidationLanguageOptions(),
      this.loadAudio()
    ]).then(() => {
      this.loading = false;
    })
  },

  filters: {
    getSegment: function (value) {
      if (!value) return 'Unknown';

      value = value.toString()
      let fileNameWithoutExtension = value.replace(/\.[^/.]+$/, "");
      let segmentString = fileNameWithoutExtension.split('---')[1];
      return segmentString;
    }
  },

  computed: {
    validatedClasses() {
      return ['grey', 'lighten-5'];
    }
  },

  methods: {
    loadValidationLanguageOptions() {
      return axios
        .get(process.env.VUE_APP_API_URL + '/languages/validationoptions')
        .then(response => {
          this.validationLanguageOptions = response.data;
        });
    },

    loadAudio() {
      return  axios
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

    pauseOtherAudios(currentFile) {
      this.audioFiles.forEach(a => {
        if (a.file_name !== currentFile) this.$refs[a.file_name][0].pause();
      });
    },

    validateAnswers() {
      this.invalidFields = false;

      let allValid = true;
      this.audioFiles = this.audioFiles.map(a => {
        if (!a.hasOwnProperty('language') || !a.language) {
          allValid = false;
        }

        return a;
      });

      this.invalidFields = !allValid;

      return allValid;
    },

    saveValidatedAudio() {
      if (this.validateAnswers()) {
        this.audioFiles.forEach(f => {
          this.$set(f, 'expected_language_code', this.$route.params.lang);
          this.$set(f, 'video_id', f.metadata.id);
          this.$set(f, 'video_title', f.metadata.title);
          delete f['metadata'];
        });

        this.loading = true;
        axios
          .post(process.env.VUE_APP_API_URL + '/audio/validated', {
            lang: this.$route.params.lang,
            data: this.audioFiles
          })
          .then(() => {
            this.snackbar = true;
            this.invalidFields = false;
            this.loadAudio().then(() => {
              this.loading = false
              window.scrollTo(0, 0);
            });
          });
      } else {
        window.scrollTo(0, 0);
      }
    },

    selectCurrentLanguageOption(file) {
      if (!file.hasOwnProperty('languages')) {
        this.$set(file, 'languages', []);
      }

      if (!file.languages.includes(this.$route.params.lang)) {
        file.languages.push(this.$route.params.lang);
      } else {
        file.languages = file.languages.filter(l => l !== this.$route.params.lang);
      }
    },

    playNextAudio(currentFileName) {
      this.audioFiles.forEach((a, i) => {
        if (a.file_name === currentFileName) {
          if (i+1 < this.audioFiles.length) {
            this.$refs[a.file_name][0].pause();
            this.$refs[this.audioFiles[i+1].file_name][0].focus();
            this.$refs[this.audioFiles[i+1].file_name][0].play();
          }
        }
      });
    }
  }
};
</script>
