import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router/auto";
import { createPinia } from "pinia";
import { Icon } from "@iconify/vue";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import App from "./App.vue";

import "@unocss/reset/tailwind.css";
import "./styles/main.css";
import "uno.css";
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
});
createApp(App).use(router).use(pinia).component("Icon", Icon).mount("#app");
