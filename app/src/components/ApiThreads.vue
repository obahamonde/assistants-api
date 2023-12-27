<script setup lang="ts">
import useStore from "~/store";
import type { ThreadResponse, GoogleUserInfo } from "~/types";
const get = useRequest<undefined, ThreadResponse[]>();
const del = useRequest<undefined, null>();
const props = defineProps<{
  user: GoogleUserInfo;
}>();
const { state } = useStore();
const getThreads = async () => {
  const { data } = await get(`/api/threads?user=${props.user.id}`, undefined, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!data.value) return;
  state.threads = data.value;
};
const postThread = async () => {
  if (!state.user) return;
  const { data } = await useFetch(`/api/threads?user=${state.user.id}`, {
    method: "POST",
    body: JSON.stringify({
      messages:[]
    }),
    headers: {
      "Content-Type": "application/json",
    },
  }).json<ThreadResponse>();
  if (!data.value) return;
  state.threads.push(data.value);
};
const deleteThread = async (id: string) => {
  await del(`/api/threads/${id}?user=${props.user.id}`, undefined, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  await getThreads();
};
onMounted(async () => {
  await getThreads();
}); 
</script>
<template>
  <section class="px-2 gap-4 col start">
    <h1 class="row center text-2xl m-4 gap-4 text-gray-700">
      <Icon
        icon="mdi-pound"
        @click="postThread()"
        class="scale cp hoverœ:text-accent x2"
      /><span>Threads</span>
    </h1>
    <section class="col start">
      <ul class="col start gap-4">
        <li v-for="thread in state.threads" class="col start animate-fade-in">
          <div
            class="row start p-4 sh"
            :class="
              state.currentThread && state.currentThread.id === thread.id
                ? 'bg-accent'
                : 'bg-primary'
            "
          >
            <Icon
              icon="mdi-pound"
              class="x4 scale cp hover:text-accent"
              @click="
                state.currentThread = thread;
                getThreads();
              "
            />
            <span class="text-md">{{ thread.title }}</span>
            <Icon
              icon="mdi-delete"
              class="scale cp hover:text-accent x2 opacity-50 hover:opacity-100 hover:text-red-500"
              @click="deleteThread(thread.id)"
            />
          </div>
        </li>
      </ul>
    </section>
  </section>
</template>
