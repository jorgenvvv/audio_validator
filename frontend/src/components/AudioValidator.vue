<template>
  <v-container>
    <v-row> Language: {{ $route.params.lang }} </v-row>
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
    <v-btn color="primary" @click="saveValidatedAudio()">Save</v-btn>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      audioFiles: []
    };
  },

  created() {
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

  methods: {
    saveValidatedAudio() {
      axios.post(process.env.VUE_APP_API_URL + '/audio/validated', {
        lang: this.$route.params.lang,
        data: this.audioFiles
      });
    }
  }
};
</script>
