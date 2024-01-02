<script setup lang="ts">
defineProps<{
  name: string;
}>();
defineEmits<{
  change: [string];
}>();
const text = ref("");
const isFocused = ref(false);
const inputRef = ref<HTMLInputElement>();
const handleFocus = () => {
  isFocused.value = true;
};
const handleBlur = () => {
  isFocused.value = false;
};
</script>
<template>
  <div class="col start mx-4 rounded-lg">
    <label
      class="text-md mx-4 my-1 font-bold"
      for="formField"
      :class="
        isFocused
          ? 'text-accent  ease-in-out duration-300'
          : text.length > 0
          ? 'text-transparent translate-y-8 text-lg ease-in-out duration-300 cursor-text'
          : 'text-accent  translate-y-8 text-lg ease-in-out duration-300 cursor-text'
      "
      @click.prevent="isFocused ? null : handleFocus()"
      >{{ name }}</label
    >
    <input
      ref="inputRef"
      type="text"
      name="formField"
      v-model="text"
      class="text-gray-500 px-4 py-2 outline-none bg-transparent border-b-2 border-gray-500"
      @change="$emit('change', text)"
      @focus="handleFocus"
      @blur="handleBlur"
    />
  </div>
</template>
<style scoped></style>
