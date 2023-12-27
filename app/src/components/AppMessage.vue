<script setup lang="ts">
import type { GoogleUserInfo, AssistantResponse, ThreadMessageResponse } from '~/types';
defineProps<{
	message: ThreadMessageResponse;
	assistant: AssistantResponse;
	user: GoogleUserInfo;
}>()
</script>
<template>
 <li class="col start"
      
      :class="message.role === 'user' ? 'end' : 'start'"
      
      >
        <div class="row start p-4" v-if="message.content && message.content.length" >
          <div v-for="block in message.content">
            <div v-if="block.type==='text' && block.text.value.length">
            <img :src="message.role  === 'user' ? user.picture : assistant.avatar" class="w-8 h-8 rounded-full m-4" />
          <AppTextBlock v-if="block.type==='text'" :content="block.text.value" />
          </div>
        </div>
        </div>
      </li>
</template>
<style scoped>

</style>