import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios";
import {uuid} from "uuidv4";

axios.defaults.baseURL= 'https://pythonweb.pl'

createApp(App).use(store).use(uuid).use(router, axios).mount('#app')
