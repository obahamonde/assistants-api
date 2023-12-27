<script setup lang="ts">
import type { AssistantRequest, FunctionDefinition } from '~/types';
defineProps<{
	assistant: AssistantRequest;
}>();
const { getFunctionCatalog, attachFunction } = useFunctions();
const definitions = ref<FunctionDefinition[]>([]);
const getDefinitions = async () => {
	const defs = await getFunctionCatalog()
	if (!defs.value) return;
	definitions.value = defs.value;
}
const index = ref<number>(0);
const sanitizedIndex = computed(() => {
  if (index.value < 0) index.value = definitions.value.length-1
  if (index.value > definitions.value.length - 1) index.value = 0
  return index.value;
});
const selectedFunction = computed(()=>{
	return definitions.value[sanitizedIndex.value] as FunctionDefinition
})
onMounted(async() => {
	await getDefinitions();
});
</script>
<template>
<div class="container mx-auto p-2 row center gap-2" v-if="selectedFunction">
    <Icon icon="mdi-chevron-left" @click="index--" class="scale-200 cp" />
		<ApiFunction :selectedFunction="selectedFunction"
		@click="attachFunction(assistant, selectedFunction)"
		/>
		<Icon icon="mdi-chevron-right" @click="index++" class="scale-200 cp" />
  </div>
</template>