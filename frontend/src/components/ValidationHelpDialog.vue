<template>
  <v-dialog v-model="storeState.helpModalVisibility" width="750">
    <v-card>
      <v-card-title class="headline">
        Validation Instructions
      </v-card-title>
      <v-divider class="mb-3"></v-divider>
      <v-card-text class="text--primary">
        <p>
          The overall goal of the validation process is to listen to different short audio clips that (should) contain speech and try to evaluate if they are from the expected language or not.
        </p>
        <p>
          To start validating choose a language that you speak from the list of <router-link to="/languages">available languages</router-link>. Then a page with short audio clips will be visible. Listen to the audio clips and choose a suitable answer / label for each clip.
        </p>
        <p>
          There are three types of answers / labels
          <ol>
            <li><i>&lt;Expected Langugage&gt;</i> - should be selected if the clip contains speech in the language that you are validating.</li>
            <li><i>Not &lt;Expected Language&gt;</i> - should be selected if the audio clip contains speech but it is in another language (not the language that you selected and are validating).</li>
            <li><i>No Speech</i> - should be selected if the audio clip contains no speech. This also includes music and singing, that might be in the correct and expected language but cannot be considered as speech.</li>
          </ol>
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
              <li><i>No Speech</i></li>
            </ol>
            Only one answer can be selected per audio clip. If the short audio segment contains speech that is in English choose the first answer (<i>English</i>). If the clip contains speech in any other language than English then choose the second answer (<i>Not English</i>). Otherwise if the audio segment did not contain andy speech at all, then choose the last answer (<i>No Speech</i>). "No Speech" should also be selected if the clip contained music or singing that was in English, because here it is not considered as speech.
            <br>
          </p>
          <p>
            For all other languages the validation process is exactly the same just the "expected" language from the clips will be different.
          </p>
        </div>
        <p> 
          Thanks for contributing!
        </p>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="closeValidationHelpDialog()">
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { store } from '../store.js';

export default {
  name: 'validation-help-dialog',
  data() {
    return {
      storeState: store.state
    };
  },

  methods: {
    closeValidationHelpDialog() {
      store.setHelpModalVisibility(false);
    }
  }
};
</script>
