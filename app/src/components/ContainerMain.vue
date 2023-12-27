<script setup lang="ts">
import type { GoogleUserInfo } from "~/types";
defineProps<{
  user: GoogleUserInfo;
}>();
</script>

<template>
  <div
    class="max-w-7xl h-screen mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center p-8"
  >
  <ApiThreadMessages :user="user" />  

  </div>
   <ApiFileObjects :user="user" />
</template>
