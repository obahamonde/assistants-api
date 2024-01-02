<script setup lang="ts">
import type { GoogleUserInfo } from "~/types";
defineProps<{
  user: GoogleUserInfo;
}>();

const show = ref<boolean>(false);
</script>

<template>
  <section>
  <Icon
      icon="mdi-apps"
      @click="show = !show"
      class="tr fixed z-50 m-2 x2 cp scale"
      :class="show ? 'text-accent' : 'text-white'"
    />
    
    <div  v-if="show">
    <ApiAssistants :user="user" class="animate-fade-in-right" /></div>
  </section>
</template>
<style scoped></style>
