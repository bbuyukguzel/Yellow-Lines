import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import Vuelidate from 'vuelidate'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './router'
import AuthPlugin from "./plugins/auth";


Vue.config.productionTip = false
Vue.use(Vuetify)
Vue.use(Vuelidate)
Vue.use(VueAxios, axios)
Vue.use(AuthPlugin);


new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
