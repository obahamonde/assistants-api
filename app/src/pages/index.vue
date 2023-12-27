<script setup lang="ts">
import useStore from "~/store";
const { state } = useStore();
const { loginWithRedirect } = useAuth();
</script>
<template>
  <AppMain :user="state.user" v-if="state.user" />

  <main v-else class="col center mt-1/4">
    <BtnGradient
      text="Get Started"
      class="scale-300"
      @click="loginWithRedirect"
    />
  </main>
</template>
<style scoped></style>
