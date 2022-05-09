import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios";
import {uuid} from "uuidv4";

axios.defaults.baseURL= 'http://172.30.0.5'

createApp(App).use(store).use(uuid).use(router, axios).mount('#app')
