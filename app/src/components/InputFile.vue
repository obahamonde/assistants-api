<script setup lang="ts">
import useStore from "~/store";
import { GoogleUserInfo } from "~/types";
const emit = defineEmits<{
  send: [string];
  see: [void];
}>();
const props = defineProps<{
  user: GoogleUserInfo;
  handler: (files: File[]) => any;
}>();
const { state } = useStore();
const onDrop = (files: File[] | null) => {
  if (files) {
    props.handler(files);
  }
};
const useInputElement = () => {
  const el = document.createElement("input");
  el.type = "file";
  el.accept = "*";
  el.multiple = true;
  el.onchange = () => {
    if (el.files) {
      props.handler(Array.from(el.files));
    }
  };
  el.click();
};
const dropZoneRef = ref<HTMLElement>();
const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);
</script>

<template>
  <section
    class="flex flex-col items-center justify-center max-w-168 mx-auto m-4"
  >
    <div
      ref="dropZoneRef"
      class="col center w-full min-h-6em bg-gray-700 h-auto rounded-lg"
      :class="isOverDropZone ? 'bg-gray-100' : 'bg-gray-600'"
    >
      <p class="flex row p-2 backdrop-blur-md gap-4">
        <Icon
          icon="mdi-attachment"
          class="text-gray-500 x3 rotate--90 cp scale"
          @click="useInputElement()"
          @click.right.prevent="$emit('see')"
        />
        <span
          class="bg-accent px-2 fixed translate-x-6 translate-y-6 col center text-xs rf"
          >{{ state.files.length }}</span
        >
        <AppRun v-slot="{ exec }">
          <InputText :user="user" :exec="exec" />

          <Icon icon="mdi-send" class="text-gray-500 x3 cp scale" @click="exec"
        /></AppRun>
      </p>
    </div>
  </section>
</template>
