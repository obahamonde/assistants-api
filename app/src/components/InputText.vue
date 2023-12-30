<script setup lang="ts">
import useStore from "~/store";
import type { GoogleUserInfo } from "~/types";
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
const postChatCompletion = (str:string) => {
  state.chatMessages.push({ content: str, role: "user" });
  state.chatMessages.push({ content: "", role: "assistant" });
  const eventSource = new EventSource(
    `/api/ai/chat/${props.user.id}?text=${str}`,
  );
  eventSource.onmessage = (event) => {
    state.chatMessages[state.chatMessages.length - 1].content += event.data;
  };
  eventSource.onerror = (event) => {
    console.log(event);
  };
  eventSource.addEventListener("done", () => {
    eventSource.close();
  });
};
const text = ref("");
</script>
<template>
  <InputVoice class="x3 cp scale" @send="postChatCompletion($event)" />
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
          : postChatCompletion(text);
        text = '';
      }
    "
    class="text-gray-500 fond-sans text-md px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent w-full max-w-144 min-w-128"
  />
</template>
