<script setup lang="ts">
import { AssistantResponse } from '~/types';

defineProps<{
	currentAssistant: AssistantResponse;
	handleClick: (assistant: AssistantResponse) => any;
	index: number;
}>();
</script>
<template>  

      <div class="image-container">
        <img :src="currentAssistant.avatar" class="rf x10 sh" :class="index%2>0 ? 'animate-flip-in-x' : 'animate-flip-in-y'"  />
        <div class="overlay">
          <p class="overlay-text">{{ currentAssistant.description }}</p>
        </div>
      </div>
    <Icon
        icon="mdi-delete"
        class="icon x2 z-50 hover:text-red hover:opacity-100 my-2 cp opacity-20"
        @click="handleClick(currentAssistant)"
      /> 
</template>
<style scoped>

</style>