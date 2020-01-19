import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';
import VueAxios from 'vue-axios';
import VueAuthenticate from 'vue-authenticate';
import axios from 'axios';

import LanguageSelect from './components/LanguageSelect';
import AudioValidator from './components/AudioValidator';
import Home from './components/Home';

import { store } from './store.js';

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.use(VueAuthenticate, {
  baseUrl: process.env.VUE_APP_API_URL,
  providers: {
    google: {
      clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
      redirectUri: process.env.VUE_APP_OAUTH2_REDIRECT_URL
    }
  },
  bindRequestInterceptor: function() {
    this.$http.interceptors.request.use(config => {
      if (this.isAuthenticated()) {
        config.headers['Authorization'] = [
          this.options.tokenType,
          this.getToken()
        ].join(' ');
      } else {
        delete config.headers['Authorization'];
      }

      return config;
    });

    this.$http.interceptors.response.use(response => {
      this.setToken(response);
      return response;
    });
  }
});

Vue.prototype.$API_URL = process.env.VUE_APP_API_URL;

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/auth/callback', name: 'auth' },
  {
    path: '/languages',
    name: 'languages',
    component: LanguageSelect,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/languages/:lang/validate',
    name: 'audiovalidator',
    component: AudioValidator,
    meta: {
      requiresAuth: true
    }
  }
];

const router = new VueRouter({
  routes
});

// Make sure that the next function is called exactly once in any given pass through the navigation guard. It can appear more than once, but only if the logical paths have no overlap, otherwise the hook will never be resolved or produce errors.
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!router.app.$auth.isAuthenticated()) {
      store.setAuthenticated(false);
      next('/');
    } else {
      next();
    }
  } else {
    if (!router.app.$auth.isAuthenticated()) store.setAuthenticated(false);

    next();
  }
});

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app');
