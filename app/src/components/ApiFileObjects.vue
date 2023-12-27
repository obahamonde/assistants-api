<script setup lang="ts">
import useStore from "~/store";
import type {
  FileObjectRequest,
  FileObjectResponse,
  GoogleUserInfo,
} from "~/types";
const props = defineProps<{
  user: GoogleUserInfo;
}>();
const { state } = useStore();
const get = useRequest<undefined, FileObjectResponse[]>();
const post = useRequest<FileObjectRequest, FileObjectResponse>();
const del = useRequest<undefined, null>();
const key = props.user.id;
const url = "/api/file_objects";
const fileObjects = ref<FileObjectResponse[]>([]);
const getFiles = async () => {
  const response = await get(`${url}?user=${key}`);
  if (!response.data.value) return;
  fileObjects.value = response.data.value;
};
const postFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await post(`${url}?user=${key}`, undefined, {
    method: "POST",
    body: formData,
  });
  if (!response.data.value) return;
  fileObjects.value.push(response.data.value);
};
const deleteFile = async (id: string) => {
  await del(`${url}/${id}?user=${key}`, undefined, {
    method: "DELETE",
  });
  await getFiles();
};
const handleUpload = async (files: File[]) => {
  const promises = files.map((file) => postFile(file));
  await Promise.all(promises);
};
const showModal = ref(false);
onMounted(getFiles);
</script>
<template>
  <InputFile
    :handler="handleUpload"
    @see="showModal = !showModal"
    :user="user"
  />
  <div
    v-if="showModal"
    class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center"
  >
    <div class="bg-white p-4 rounded-lg shadow-lg max-w-lg w-full">
      <h2 class="text-lg font-semibold mb-4">File Gallery</h2>
      <div class="grid grid-cols-2 gap-4">
        <div
          v-for="file in fileObjects"
          :key="file.id"
          class="border p-2 rounded"
        >
          <img
            :src="file.url"
            alt="file.filename"
            class="h-20 w-20 object-cover mb-2"
          />
          <p>{{ file.filename }}</p>
          <Icon
            :icon="
              state.files && state.files.includes(file)
                ? 'mdi-check'
                : 'mdi-plus'
            "
            class="opacity-50 text-primary hover:opacity-100 hover:text-accent"
            @click="
              state.files.includes(file)
                ? state.files.splice(state.files.indexOf(file), 1)
                : state.files.push(file)
            "
          />

          <Icon
            icon="mdi-delete"
            @click="deleteFile(file.id)"
            class="opacity-50 text-warning hover:opacity-100 hover:text-red-500"
            >Delete</Icon
          >
        </div>
      </div>
      <button
        @click="showModal = false"
        class="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Close
      </button>
    </div>
  </div>
</template>
<style scoped></style>
