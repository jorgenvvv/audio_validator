<template>
  <v-container>
    <v-list>
      <v-row>
        <v-col
          v-for="lang in availableLanguages"
          :key="lang.code"
          cols="12"
          sm="6"
        >
          <v-list-item @click="chooseLanguage(lang.code)">
            <v-list-item-content>
              <v-list-item-title class="d-inline-flex justify-space-between">
                <span>{{ lang.name }} ({{ lang.nativeName }})</span>

                <span class="caption"
                  >({{ lang.validated }} / {{ lang.total }})</span
                >
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-progress-linear
                  :value="validatedPercentage(lang.total, lang.validated)"
                  height="25"
                >
                  <strong
                    >{{
                      validatedPercentage(lang.total, lang.validated)
                    }}%</strong
                  >
                </v-progress-linear>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
  </v-container>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      availableLanguages: [],
      selectedLanguage: null
    };
  },

  created() {
    axios.get(process.env.VUE_APP_API_URL + '/languages/all').then(response => {
      this.availableLanguages = response.data;
    });
  },

  methods: {
    chooseLanguage(langCode) {
      this.$router.push({ name: 'audiovalidator', params: { lang: langCode } });
    },

    validatedPercentage(total, validated) {
      return ((validated / total) * 100).toFixed(1);
    }
  }
};
</script>
