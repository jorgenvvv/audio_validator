<template>
  <v-container>
    <language-skill-dialog v-if="languageSkillDialogVisible" :language="currentLanguage.name" @save="saveLanguageSkill"></language-skill-dialog>
    <v-row>
      <v-col cols="12">
        <v-card class="pl-2" v-if="currentLanguage.name">
          <v-row>
            <v-col class="d-flex">
              <div class="d-flex flex-grow-1 flex-column text-center">
                <div class="flex-grow-1">
                  <p class="ma-0 mb-2 font-weight-bold">Selected Language</p>
                  <p class="ma-0 mb-2 caption">
                    {{ currentLanguage.name }} ({{ currentLanguage.nativeName }})
                  </p>
                </div>
                <div>
                  <v-btn text small color="primary" @click="$router.push('/languages')">Change Language</v-btn><br>
                  <v-btn text small color="primary" @click="openValidationHelpDialog()">View validation Instructions</v-btn>
                </div>
              </div>
            </v-col>
            <v-divider vertical></v-divider>
            <v-col class="d-flex">
              <div class="d-flex flex-grow-1 flex-column text-center">
                <div class="flex-grow-1">
                  <p class="ma-0 mb-2 font-weight-bold">Your Statistics</p>
                  <p class="ma-0 mb-1 caption">
                    Ranking: {{ ordinalRank }} place / {{ userValidationStats.usersCount }} total users
                  </p>
                  <p class="ma-0 caption">
                    Validated clips: {{ userValidationStats.languageValidatedCount }} {{ currentLanguage.name }} / {{ userValidationStats.totalValidatedCount }} all languages
                  </p>
                </div>
                <div>
                  <p class="ma-0"><v-btn text small color="primary" @click="openLeaderboardDialog()">View All Scores</v-btn></p>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-alert
      v-if="audioFiles.length === 0 && !loading"
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      There is no more audio to validate for selected language.
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

      <div
        :class="file.language ? validatedClasses : ''"
        v-for="file of audioFiles"
        :key="file.file_name"
      >
        <v-row
          @keyup.78="playNextAudio(file.file_name)"
        >
          <v-col cols="12" sm="8">
            <v-row class="pl-2 pl-sm-6 py-2" v-if="file.metadata">
              <v-col>
                <div>{{ file.metadata.title }}</div>
                <div class="caption">
                  Segment: {{ file.file_name | getSegment }}
                </div>
              </v-col>
            </v-row>
            <v-row class="pl-2 pl-sm-6">
              <v-row>
                <div class="ml-6">
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
          <v-col cols="12" sm="4">
            <v-row class="ml-2">
              <v-radio-group v-model="file.language" column>
                <template v-slot:label>
                  <div class="overline">Select spoken language</div>
                </template>
                <v-radio
                  :label="currentLanguage.name"
                  value="GIVEN_LANG"
                ></v-radio>
                <v-radio
                  :label="'Not ' + currentLanguage.name"
                  value="NOT_GIVEN_LANG"
                ></v-radio>
                <v-radio label="No speech" value="NO_SPEECH"></v-radio>
                <v-radio label="Don't know" value="DO_NOT_KNOW"></v-radio>
              </v-radio-group>
            </v-row>
          </v-col>
        </v-row>
        <v-divider></v-divider>
      </div>
      <div class="d-flex flex-row-reverse">
        <v-btn class="ma-4" color="primary" @click="saveValidatedAudio()"
          >Save</v-btn
        >
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
import { store } from '../store.js';
import { ordinal } from '../utils.js'
import { EventBus } from '../event-bus.js';

import axios from 'axios';
import LanguageSkillDialog from './LanguageSkillDialog';

export default {
  components: {
    LanguageSkillDialog
  },

  data() {
    return {
      storeState: store.state,
      audioFiles: [],
      invalidFields: false,
      currentLanguage: {},
      snackbar: false,
      loading: false,
      languageSkillDialogVisible: false,
      userLanguageSkill: null,
      userValidationStats: {}
    };
  },

  created() {
    this.loading = true;
    axios
      .all([
        this.loadAudio(),
        this.loadCurrentLanguage(),
        this.loadUserLanguageSkill(),
        this.loadUserValidatedAudioCount()
      ])
      .then(() => {
        this.loading = false;
      });
  },

  filters: {
    getSegment: function(value) {
      if (!value) return 'Unknown';

      value = value.toString();
      let fileNameWithoutExtension = value.replace(/\.[^/.]+$/, '');
      let segmentString = fileNameWithoutExtension.split('---')[1];
      return segmentString;
    }
  },

  computed: {
    validatedClasses() {
      return ['grey', 'lighten-5'];
    },

    ordinalRank() {
      if (this.userValidationStats.rank === 1)
        return '🥇 ' + ordinal(this.userValidationStats.rank);
      else if (this.userValidationStats.rank === 2)
        return '🥈 ' + ordinal(this.userValidationStats.rank);
      else if (this.userValidationStats.rank === 3)
        return '🥉 ' + ordinal(this.userValidationStats.rank);

      return ordinal(this.userValidationStats.rank);
    }
  },

  methods: {
    loadAudio() {
      return axios
        .get(
          process.env.VUE_APP_API_URL +
            '/audio/' +
            this.$route.params.lang +
            '/all'
        )
        .then(response => {
          this.audioFiles = response.data;
        });
    },

    loadCurrentLanguage() {
      return axios
        .get(
          process.env.VUE_APP_API_URL +
            '/languages/' +
            this.$route.params.lang +
            '/info'
        )
        .then(response => {
          this.currentLanguage = response.data;
        });
    },

    loadUserLanguageSkill() {
      return axios
        .get(
          process.env.VUE_APP_API_URL + '/user/skill/' + this.$route.params.lang
        )
        .then(response => {
          this.userLanguageSkill = response.data.skillLevel;
          if (!this.userLanguageSkill) {
            this.languageSkillDialogVisible = true;
          }
        });
    },

    loadUserValidatedAudioCount() {
      axios
        .get(
          process.env.VUE_APP_API_URL +
            '/user/validated/' +
            this.$route.params.lang
        )
        .then(response => {
          this.userValidationStats = response.data;
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

    saveLanguageSkill(skillLevel) {
      this.userLanguageSkill = skillLevel;
      this.languageSkillDialogVisible = false;
    },

    saveValidatedAudio() {
      if (this.validateAnswers()) {
        this.audioFiles.forEach(f => {
          this.$set(f, 'expected_language_code', this.$route.params.lang);
          this.$set(f, 'video_id', f.metadata.id);
          this.$set(f, 'video_title', f.metadata.title);
          this.$set(f, 'validator_skill_level', this.userLanguageSkill);
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
              this.loading = false;
              window.scrollTo(0, 0);
            });
            this.loadUserValidatedAudioCount();
            EventBus.$emit('update-leaderboard');
          });
      } else {
        window.scrollTo(0, 0);
      }
    },

    playNextAudio(currentFileName) {
      this.audioFiles.forEach((a, i) => {
        if (a.file_name === currentFileName) {
          if (i + 1 < this.audioFiles.length) {
            this.$refs[a.file_name][0].pause();
            this.$refs[this.audioFiles[i + 1].file_name][0].focus();
            this.$refs[this.audioFiles[i + 1].file_name][0].play();
          }
        }
      });
    },

    openValidationHelpDialog() {
      store.setHelpModalVisibility(true);
    },

    openLeaderboardDialog() {
      store.setLeaderboardDialogVisibility(true);
    }
  }
};
</script>
<style scoped>
audio {
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
  border-radius: 90px;
}
</style>