<script setup lang="ts">
import type { FunctionDefinition } from "~/types";
import useStore from "~/store";
defineProps<{
  selectedFunction: FunctionDefinition;
}>();
const { state } = useStore();
const show = ref(false);
const { attachFunction } = useFunctions();
</script>
<template>
  <article class="flex flex-col items-center justify-around card bg-gray-500 h-72 w-full" v-if="selectedFunction">
    
      <h2 class="text-lg text-cyan-300">
        {{
          selectedFunction.name[0].toUpperCase() +
          selectedFunction.name.slice(1)
        }}
      </h2>
      <p class="text-caption rounded-md px-4 py-2">
        {{ selectedFunction.description.trim() }}
      </p>
      <div class="gap-1 mt-2 grid2">
        <span
          v-for="(_, key) in selectedFunction.parameters.properties"
          :key="key"
          class="btn-pill"
        >
          {{ key }}:<strong class="text-amber">{{ _.type }}</strong>
        </span>
      </div>
       <footer class="row center">
         <button title="Show Tool Schema">
        <Icon icon="mdi-code-tags" @click="show = !show" class="btn-icon shadow-btn" /></button>
        <button title="Attach Tool to Assistant" v-if="state.assistantRequest"
        @click="attachFunction(state.assistantRequest,selectedFunction)"
        >
        <Icon icon="fluent:bot-add-20-filled" @click="show = !show" class="btn-icon shadow-btn"/></button></footer>
  </article>
      <AppFunction :definition="selectedFunction" @close="show=false" v-if="show" />
</template>
<style scoped>

</style>
