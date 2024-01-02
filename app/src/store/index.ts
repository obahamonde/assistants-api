import { defineStore, acceptHMRUpdate } from "pinia";
import type {
  GoogleUserInfo,
  AssistantResponse,
  ThreadMessageResponse,
  ThreadResponse,
  RunResponse,
  FileObjectResponse,
  AssistantRequest,
} from "~/types";
const useStore = defineStore("state", () => {
  const state = {
    token: "",
    user: null as GoogleUserInfo | null,
    currentAssistant: null as AssistantResponse | null,
    currentThread: null as ThreadResponse | null,
    threads: [] as ThreadResponse[],
    run: null as RunResponse | null,
    messages: [] as ThreadMessageResponse[],
    files: [] as FileObjectResponse[],
    assistantRequest: {} as AssistantRequest | null,
    chatMessages: [] as { content: string; role: "user" | "assistant" }[],
  };
  return {
    state,
  };
});
if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));

export default useStore;
