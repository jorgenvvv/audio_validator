<template>
  <v-container>
    <language-skill-dialog v-if="languageSkillDialogVisible" :language="currentLanguage.name" @save="saveLanguageSkill"></language-skill-dialog>
    <v-expansion-panels class="mb-2">
      <v-expansion-panel>
        <v-expansion-panel-header class="subtitle-1 font-weight-bold">
          Validation Instructions
        </v-expansion-panel-header>
        <v-expansion-panel-content class="body-2">
          <p>
            The overall goal of the validation process is to listen to different short audio clips that (should) contain speech and try to evaluate if they are from the expected language or not.
          </p>
          <p>
            To start validating choose a language that you speak from the list of <router-link to="/languages">available languages</router-link>. Then a page with short audio clips will be visible. Listen to the audio clips and choose a suitable answer / label for each clip.
          </p>
          <p>
            There are three types of answers / labels
            <ol>
              <li><i>&lt;Expected langugage&gt;</i> - should be selected if the clip contains speech in the language that you are validating.</li>
              <li><i>Not &lt;expected language&gt;</i> - should be selected if the audio clip contains speech but it is in another language (not the language that you selected and are validating).</li>
              <li><i>No speech</i> - should be selected if the audio clip contains no speech. This also includes music and singing, that might be in the correct and expected language but cannot be considered as speech.</li>
              <li><i>Don't know</i> - should be selected if it is not possible to understand the spoken language in the clip (for example the audio segment is very short or contains too much noise).</li>
            </ol>
            If an audio clip contains speech in multiple languages (or music and speech in the same clip) then please try to choose an answer according to the language that has the "majority" in the clip. For example, if a clip contains a sentence Spanish and then the rest of the conversation is in English then English is the correct answer.
          </p>
          <p>
            All clips on the page must be labelled and then you can press "Save". After that the answers are saved and you will be given a new set of audio clips to validate.
          </p>
          <div class="elevation-2 pa-2 mb-3">
            <span class="subtitle-2">Example</span>
            <p>
            If the language that you chose and started validating was English then the available answers will be
              <ol>
                <li><i>English</i></li>
                <li><i>Not English</i></li>
                <li><i>No speech</i></li>
                <li><i>Don't know</i></li>
              </ol>
              Only one answer can be selected per audio clip. If the short audio segment contains speech that is in English choose the first answer (<i>English</i>). If the clip contains speech in any other language than English then choose the second answer (<i>Not English</i>). If the audio segment did not contain andy speech at all, then choose the third answer (<i>No speech</i>). "No speech" should also be selected if the clip contained music or singing that was in English, because here it is not considered as speech. And finally, if an audio clip contains spoken language, but it is not possible to understand, then choose the last answer (<i>Don't know</i>).
              <br>
            </p>
            <p>
              For all other languages the validation process is exactly the same just the "expected" language from the clips will be different.
            </p>
          </div>
          <p> 
            Thanks for contributing!
          </p>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-card class="pa-2 pl-6 mb-2" v-if="currentLanguage.name">
      <b>Selected Language</b>: {{ currentLanguage.name }} ({{ currentLanguage.nativeName }})
      <v-btn text small color="primary" @click="$router.push('/languages')">Change</v-btn>
    </v-card>
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
import axios from 'axios';
import LanguageSkillDialog from './LanguageSkillDialog';

export default {
  components: {
    LanguageSkillDialog
  },

  data() {
    return {
      audioFiles: [],
      invalidFields: false,
      currentLanguage: {},
      snackbar: false,
      loading: false,
      languageSkillDialogVisible: false,
      userLanguageSkill: null,
    };
  },

  created() {
    this.loading = true;
    axios.all([this.loadAudio(), this.loadCurrentLanguage(), this.loadUserLanguageSkill()]).then(() => {
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
          this.userLanguageSkill = response.data;
          if (!this.userLanguageSkill) {
            this.languageSkillDialogVisible = true;
          }
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