import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

Vue.prototype.$API_URL = process.env.VUE_APP_API_URL;

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
