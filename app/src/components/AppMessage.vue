<script setup lang="ts">
import type {
  GoogleUserInfo,
  AssistantResponse,
  ThreadMessageResponse,
} from "~/types";
defineProps<{
  message: ThreadMessageResponse;
  assistant: AssistantResponse;
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
  <li class="col start" :class="message.role === 'user' ? 'end' : 'start'" w>
    <div class="row start p-4" v-if="message.content && message.content.length">
      <div v-for="block in message.content">
        <div v-if="block.type === 'text' && block.text.value.length">
          <img
            :src="message.role === 'user' ? user.picture : assistant.avatar"
            class="w-8 h-8 rounded-full m-4"
          />
          <Icon
            icon="mdi-play-circle"
            class="w-8 h-8 rounded-full m-4"
            v-if="message.role === 'assistant' && block.text.value.length"
            @click="playAudio(block.text.value)"
          />
          <AppTextBlock
            v-if="block.type === 'text'"
            :content="block.text.value"
          />
        </div>
      </div>
    </div>
  </li>
</template>
<style scoped></style>
