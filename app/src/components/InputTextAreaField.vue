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
          : 'text-accent  translate-y-12 text-lg ease-in-out duration-300 cursor-text'
      "
      @click.prevent="isFocused ? null : handleFocus()"
      >{{ name }}</label
    >
    <textarea
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
<style scoped>
/* Customizes the scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 12px; /* Width of the scrollbar */
}

/* Styles for the scrollbar track (background) */
::-webkit-scrollbar-track {
  background: transparent; /* Transparent track background */
}

/* Styles for the scrollbar thumb (the part that you drag) */
::-webkit-scrollbar-thumb {
  background: linear-gradient(
    to bottom,
    #17b9ac,
    #aced7c
  ); /* Gradient from cyan to navy */
  border-radius: 6px; /* Optional: Adds rounded corners to the scrollbar thumb */
}

/* Styles for the scrollbar thumb when hovered or active */
::-webkit-scrollbar-thumb:hover,
::-webkit-scrollbar-thumb:active {
  background: linear-gradient(
    to bottom,
    #17b9ac,
    #aced7c
  ); /* Slightly darker gradient for hover/active states */
}
</style>
