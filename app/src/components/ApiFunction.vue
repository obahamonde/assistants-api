<script setup lang="ts">
import type { FunctionDefinition } from '~/types';
defineProps<{
	selectedFunction: FunctionDefinition;
}>();
const show = ref(false);
</script>
<template>
  <div class="card bg-gray-500 h-72">
      <h2 class="text-title">{{ selectedFunction.name[0].toUpperCase()+selectedFunction.name.slice(1) }}</h2>
      <p class=" text-caption rounded-md px-4 py-2">{{ selectedFunction.description.trim() }}</p>
      <div class="gap-2 mt-2 grid2">
        <!-- Property pills -->
        <span v-for="(_, key) in selectedFunction.parameters.properties" :key="key" class="bg-accent text-xs rounded-3xl p-2">
          {{ key }}:<strong class="text-amber">{{ _.type  }}</strong> 
        </span>
				
      </div>
			<!-- Button to open modal -->
			<BtnGradient text="Show Schema" @click="show=true" class="mt-4" />
		</div>

		<!-- Modal -->
		<div v-if="show" class="modal">
			<div class="modal-content">
				<span @click="show=false" class="close">&times;</span>
				<pre>{{ JSON.stringify(selectedFunction, null, 2) }}</pre>
			</div>	</div>
	
</template>
<style scoped>
.card {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color:navy;
  margin: 15% auto;
  padding: 4rem;
  border: 1px solid #888;
	color: #cf0;
  width: 50%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: red;
  text-decoration: none;
  cursor: pointer;
}
</style>