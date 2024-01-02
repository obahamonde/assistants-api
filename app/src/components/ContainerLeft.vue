<script setup lang="ts">
import type { GoogleUserInfo } from "~/types";
const show = ref(false);
defineProps<{
  user: GoogleUserInfo;
}>();
</script>
<template>
  <Icon
    icon="mdi-menu"
    @click="show = !show"
    class="x2 tl fixed z-50 scale cp m-2"
    :class="
      show
        ? 'translate-x-48 ease-in-out duration-500 text-gray-700'
        : 'text-white'
    "
  />
  <section
    class="h-screen w-80 tl animate-fade-in-left duration-500 bg-gradient-to-b from-teal-500 to-lime-300 via-cyan-400"
    v-if="show"
  >
    <ApiThreads :user="user" />
    <ApiUser :user="user" />
  </section>
</template>
<style scoped></style>
