<script setup lang="ts">
const lang = ref<'en-US'|'es-ES' | 'es-MX'>('en-US')
const { start, stop, result, isListening } = useSpeechRecognition({
	lang:lang
})
const emit = defineEmits<{
	send:[string]
}>()
const $stop = () => {
	stop()
	emit('send', result.value)
	result.value = ''
}
</script>
<template>
<Icon :icon="!isListening ?'mdi-microphone' : 'mdi-microphone-off'" :class="isListening ? 'text-red-500' : 'text-gray-500'" @click="isListening ? $stop(): start()" class="x2 rf p-1x`x cp scale" />
</template>