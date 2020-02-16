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
          <v-col class="mt-5 d-flex justify-center" v-if="languagesLoading">
            <v-progress-circular
              :size="50"
              color="primary"
              indeterminate
            ></v-progress-circular>
          </v-col>
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
      allLanguages: {},
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
        },
        {
          text: 'Most Validated',
          value: 'MOST_VALIDATED'
        },
        {
          text: 'Least Validated',
          value: 'LEAST_VALIDATED'
        }
      ],
      sortOrder: null,
      languagesLoading: false
    };
  },

  created() {
    this.languagesLoading = true;
    axios.get(process.env.VUE_APP_API_URL + '/languages/all').then(response => {
      this.allLanguages = response.data;
      for (let [key, value] of Object.entries(this.allLanguages)) {
        let tmpValue = value;
        tmpValue['code'] = key;
        this.availableLanguages.push(tmpValue)
      }
      this.availableLanguages.sort((a, b) => a.name.localeCompare(b.name));
      this.languagesLoading = false;
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

      if (this.sortOrder === 'MOST_VALIDATED')
        this.availableLanguages.sort((a, b) => b.validated - a.validated);

      if (this.sortOrder === 'LEAST_VALIDATED')
        this.availableLanguages.sort((a, b) => a.validated - b.validated);
    }
  }
};
</script>
