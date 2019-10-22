import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'

import LanguageSelect from './components/LanguageSelect';
import AudioValidator from './components/AudioValidator'

Vue.config.productionTip = false

Vue.use(VueRouter)

Vue.prototype.$API_URL = process.env.VUE_APP_API_URL

const routes = [
  { path: '/', component: LanguageSelect },
  { path: '/:lang/validate', component: AudioValidator }
]

const router = new VueRouter({
  routes
})

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
