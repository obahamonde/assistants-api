<script setup lang="ts">
import useStore from "~/store";
import type { ThreadRequest, ThreadResponse, GoogleUserInfo } from "~/types";
import type { ThreadMessageRequest, ThreadMessageResponse } from "~/types";
const postThis = useRequest<ThreadMessageRequest, ThreadMessageResponse>();
const props = defineProps<{
  user: GoogleUserInfo;
  exec: () => any;
}>();
const { state } = useStore();
const postThreadMessage = async (message: ThreadMessageRequest) => {
  if (!props.user) return;
  const { data } = await postThis(
    `/api/thread_messages?user=${props.user.id}`,
    message,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
  if (!data.value) return;
  state.messages.push(data.value);
   await props.exec()
};
const post = useRequest<ThreadRequest, ThreadResponse>();
const postThread = async (thread: ThreadRequest) => {
  if (!state.user) return;
  const { data } = await post(`/api/threads?user=${state.user.id}`, thread, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!data.value) return;
  state.threads.push(data.value);
 
};

const text = ref("");
const threadRequest = ref<ThreadRequest>({
  messages: [{ content: text.value, role: "user" }],
});
</script>
<template>
  <input
    type="text"
    v-model="text"
    @keyup.enter="
      () => {
        if (!text.length) return;
        state.currentThread
          ? postThreadMessage({
              thread_id: state.currentThread.id,
              content: text,
              role: 'user',
              file_ids: state.files.map((file) => {
                return file.id;
              }),
            })
          : postThread(threadRequest);
        text = '';
      }
    "
    class="text-gray-500 fond-sans text-md px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent w-full max-w-144 min-w-128"
  />
</template>
