import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import './style.css';
import App from './App.vue';
import pinia from './stores';
import router from './router';
import { useUserStore } from './stores/user';

const app = createApp(App);

app.use(ElementPlus);
app.use(pinia);
app.use(router);

// 恢复登录状态：有 token 则从后端拉取用户信息
const userStore = useUserStore();
userStore.fetchProfile();

app.mount('#app');
