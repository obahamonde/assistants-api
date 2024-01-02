<script setup lang="ts">
import type { FunctionDefinition } from '~/types';
defineProps<{
	definition: FunctionDefinition;
}>();
</script>
<template>
	<div class="modal">
    <div class="modal-content">
      <span @click="$emit('close')" class="close">&times;</span>
<pre class="text-white">
{{ JSON.stringify(Object.fromEntries(Object.entries(definition).map(([key, value]) => {
	//@ts-ignore
	if (key === 'description') return [key, value.trim()];
	return [key, value];
})), null, 2) }}
</pre>
 </div>
	</div>
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
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: navy;
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