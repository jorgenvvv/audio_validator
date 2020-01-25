<template>
  <v-container>
    <v-item-group>
      <v-container>
        <v-row no-gutters class="justify-end mb-3">
          <v-col cols="12" sm="4" md="3">
            <v-select
              @change="sortLanguages()"
              v-model="sortOrder"
              :items="sortOptions"
              label="Sort By"
              solo
              dense
              hide-details
            ></v-select>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
          <v-col
            v-for="lang in availableLanguages"
            :key="lang.code"
            cols="12"
            sm="6"
            md="4"
          >
            <v-item>
              <v-card @click="chooseLanguage(lang.code)">
                <v-card-title class="subtitle-1 justify-space-between">
                  <span>{{ lang.name }} ({{ lang.nativeName }})</span>

                  <span class="caption"
                    >({{ lang.validated }} / {{ lang.total }})</span
                  >
                </v-card-title>
                <v-card-text>
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
                </v-card-text>
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
  </v-container>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      availableLanguages: [],
      selectedLanguage: null,
      sortOptions: [
        {
          text: 'Language - Ascending',
          value: 'LANGUAGE_ASC'
        },
        {
          text: 'Language - Descending',
          value: 'LANGUAGE_DESC'
        }
      ],
      sortOrder: null
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
    },

    sortLanguages() {
      if (this.sortOrder === 'LANGUAGE_ASC')
        this.availableLanguages.sort((a, b) => a.name.localeCompare(b.name));

      if (this.sortOrder === 'LANGUAGE_DESC')
        this.availableLanguages.sort((a, b) => b.name.localeCompare(a.name));
    }
  }
};
</script>
