<script setup lang="ts">
import type { GoogleUserInfo } from '~/types';
type ChatMessage = {
	content: string;
	role: string;
};
defineProps<{
	messages: ChatMessage[];
	user: GoogleUserInfo;
}>()
</script>
<template>
 
        <div class="col start p-4" >
          <div v-for="message in messages">
            <img :src="message.role  === 'user' ? user.picture : 'https://e7.pngegg.com/pngimages/811/700/png-clipart-chatbot-internet-bot-business-natural-language-processing-facebook-messenger-business-people-logo-thumbnail.png'" class="w-8 h-8 rounded-full m-4" />
          <AppTextBlock  :content="message.content" />
          </div>
        </div>
</template>
<style scoped>

</style>