import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import Vuelidate from 'vuelidate'

Vue.config.productionTip = false
Vue.use(Vuetify, Vuelidate)

new Vue({
  render: h => h(App),
}).$mount('#app')
