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
              <li><i>&lt;Expected langugage&gt;</i> - should be selected if the clip contains speech in the language that you are validating.</li>
              <li><i>Not &lt;expected language&gt;</i> - should be selected if the audio clip contains speech but it is in another language (not the language that you selected and are validating).</li>
              <li><i>No speech</i> - should be selected if the audio clip contains no speech. This also includes music and singing, that might be in the correct and expected language but cannot be considered as speech.</li>
              <li><i>Don't know</i> - should be selected if it is not possible to understand the spoken language in the clip (for example the audio segment is very short or contains too much noise) or if it is just very hard to choose another answer (for example multiple languages are equally present in the audio clip).</li>
            </ol>
          </p>
          <p>
            If an audio clip contains speech in multiple languages (or music and speech in the same clip) then please try to choose an answer according to the language that has the "majority" in the clip. For example, if a clip contains a sentence Spanish and then the rest of the conversation is in English then English is the correct answer. If the clip contains voiced over audio and both languages are equally present then it really is hard to choose a correct answer. In these cases the "I don't know" answer should be selected.
          </p>
          <p>
            All clips on the page must be labelled and then you can press "Save". After that the answers are saved and you will be given a new set of audio clips to validate.
          </p>
          <p>There is pretty much an unlimited amount of audio clips to validate. So you can validate as many clips as you can :).</p>
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
