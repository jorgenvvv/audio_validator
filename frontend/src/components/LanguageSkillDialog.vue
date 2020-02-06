<template>
  <v-dialog :value="true" width="600" persistent>
    <v-card>
      <v-card-title class="headline">
        Language Proficiency
      </v-card-title>
      <v-divider class="mb-3"></v-divider>
      <v-card-text class="text--primary">
        <div class="body-1">
          Please rate your language proficiency in <b>{{ language }}</b
          > in the context of spoken language recognition.
        </div>
        <div>
          <v-radio-group v-model="languageSkillLevel" column>
            <v-radio value="1">
              <template v-slot:label>
                <v-icon>mdi-numeric-1-box</v-icon> - I do not recognize the language at all
              </template>
            </v-radio>
            <v-radio value="2">
              <template v-slot:label>
                <v-icon>mdi-numeric-2-box</v-icon> - If the speech is very clear I
                do recognize the language
              </template>
            </v-radio>
            <v-radio value="3">
              <template v-slot:label>
                <v-icon>mdi-numeric-3-box</v-icon> - In most cases I recognize the language
              </template>
            </v-radio>
            <v-radio value="4">
              <template v-slot:label>
                <v-icon>mdi-numeric-4-box</v-icon> - I speak the language
              </template>
            </v-radio>
            <v-radio value="5">
              <template v-slot:label>
                <v-icon>mdi-numeric-5-box</v-icon> - It is my native language
              </template>
            </v-radio>
          </v-radio-group>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <router-link to="/languages">
          <v-btn
            text
          >
            Cancel
          </v-btn>
        </router-link>
        <v-btn
          color="primary"
          text
          @click="saveLanguageProficiency()"
          :disabled="!languageSkillLevel"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'language-skill-dialog',

  props: {
    language: String
  },

  data() {
    return {
      languageSkillLevel: null
    };
  },

  methods: {
    saveLanguageProficiency() {
      this.$emit('save', this.languageSkillLevel);
    }
  }
};
</script>
<style scoped>
a {
  text-decoration: none;
}
</style>