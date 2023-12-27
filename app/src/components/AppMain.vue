<script setup lang="ts">
import type { GoogleUserInfo } from "~/types";
defineProps<{
  user: GoogleUserInfo;
}>();
</script>
<template>
  <div class="h-screen flex row">
    <ContainerLeft :user="user" />
    <div class="col center w-full">
      <ContainerMain :user="user" />
    </div>
    <ContainerRight :user="user" />
  </div>
</template>
<style scoped></style>
