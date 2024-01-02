<script setup lang="ts">
import type { GoogleUserInfo } from "~/types";
type ChatMessage = {
  content: string;
  role: string;
};
defineProps<{
  messages: ChatMessage[];
  user: GoogleUserInfo;
}>();

const playAudio = async (text: string) => {
  const response = await fetch(`/api/ai/audio?text=${text}`);
  const arrayBuffer = await response.arrayBuffer();
  const audio = new Audio(URL.createObjectURL(new Blob([arrayBuffer])));
  audio.play();
};
</script>
<template>
  <div class="col start p-4">
    <div v-for="message in messages">
      <div class="row" :class="message.role === 'user' ? 'end' : 'start'">
        <img
          :src="
            message.role === 'user'
              ? user.picture
              : 'https://e7.pngegg.com/pngimages/811/700/png-clipart-chatbot-internet-bot-business-natural-language-processing-facebook-messenger-business-people-logo-thumbnail.png'
          "
          class="w-8 h-8 rounded-full m-4"
        />
        <Icon
          icon="mdi-play-circle"
          class="w-8 h-8 rounded-full m-4 cp scale hover:bg-blend-darken"
          v-if="message.role === 'assistant' && message.content.length"
          @click="playAudio(message.content)"
        />
      </div>
      <AppTextBlock :content="message.content" />
    </div>
  </div>
</template>
<style scoped></style>
