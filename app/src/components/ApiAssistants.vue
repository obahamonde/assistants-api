<script setup lang="ts">
import useStore from "~/store";
import type {
  AssistantRequest,
  ToolAssistantToolsFunction,
  AssistantResponse,
  GoogleUserInfo,
} from "~/types";
const loading = ref<boolean>(false);
const get = useRequest<undefined, AssistantResponse[]>();
const post = useRequest<AssistantRequest, AssistantResponse>();
const del = useRequest<undefined, null>();
const put = useRequest<AssistantResponse, AssistantResponse>();
const props = defineProps<{
  user: GoogleUserInfo;
}>();
const { state } = useStore();
const key = props.user.id;
const url = "/api/assistants";
const assistants = ref<AssistantResponse[]>([]);
const assistantRequest = reactive<AssistantRequest>({
  model:"gpt-4-1106-preview",
  name: "",
  description: "",
  instructions: "",
  file_ids: state.files.map((file) => {
    return file.id;
  }),
  tools: [] as ToolAssistantToolsFunction[],
});
const getAssistants = async () => {
  loading.value = true;
  const response = await get(`${url}?user=${key}`);
  if (!response.data.value) return;
  assistants.value = response.data.value;
  loading.value = false;
};
const postAssistant = async (assistant: AssistantRequest) => {
  loading.value = true;
  if (assistant.name.length === 0) return;
  if (!assistant.description || assistant.description.length === 0) return;
  if (!assistant.instructions || assistant.instructions.length === 0) return;
  const response = await post(`${url}?user=${key}`, assistant, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.data.value) return;
  assistants.value.push(response.data.value);
  assistantRequest.name = "";
  assistantRequest.description = "";
  assistantRequest.instructions = "";
  loading.value = false;  
};
const deleteAssistant = async (id: string) => {
  await del(`${url}/${id}?user=${key}`, undefined, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });
  //await getAssistants();
};
// @ts-ignore
const putAssistant = async (assistant: AssistantResponse) => {
  const response = await put(`${url}/${assistant.id}?user=${key}`, assistant, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.data.value) return;
  await getAssistants();
};

const index = ref<number>(0);
const sanitizedIndex = computed(() => {
  if (index.value < 0) index.value = assistants.value.length-1
  if (index.value > assistants.value.length - 1) index.value = 0
  return index.value;
});
const currentAssistant = computed(()=>{
	return assistants.value[sanitizedIndex.value] as AssistantResponse
})
onMounted(async () => {
  await getAssistants();
});
watchEffect(()=>state.currentAssistant=currentAssistant.value)
</script>
<template>
  <aside
    class="w-full md:w-80 h-full fixed right-0 top-0 flex flex-col bg-gradient-to-b from-teal-500 to-lime-300 via-cyan-400 text-navy"
  >
    <section class="flex-1 p-4 overflow-hidden">
    <div class="col center p-4">
    <div class="row center" v-if="state.currentAssistant">
      <Icon icon="mdi-chevron-left" @click="index--" class="scale-200 cp" v-if="!loading" />
      <div class="image-container">
        <img :src="currentAssistant.avatar" class="rf x10 sh" :class="index%2>0 ? 'animate-flip-in-x' : 'animate-flip-in-y'" v-if="!loading" />
        <div class="overlay">
          <p class="overlay-text">{{ currentAssistant.description }}</p>
        </div>
      </div>
      <Icon icon="mdi-loading" v-if="loading" class="x4 text-accent animate-spin" />
      <Icon icon="mdi-chevron-right" @click="index++" 
      v-if="!loading"
      class="scale-200 cp" />
    </div>
      <Icon
        icon="mdi-delete"
        class="icon x2 z-50 hover:text-red hover:opacity-100 my-2 opacity-50"
        @click="deleteAssistant(currentAssistant.id)"
      />
    </div>
  </section>
  <FunctionCatalogue :assistant="assistantRequest" />
    <section class="flex-1 p-4">
      <form @submit.prevent="postAssistant(assistantRequest)" class="col center p-4">
        <InputFormField name="Name" @change="assistantRequest.name = $event" />
        <InputTextAreaField
          name="Description"
          @change="assistantRequest.description = $event" />
        <InputTextAreaField
          name="Instructions"
          @change="assistantRequest.instructions = $event" />
          <div dropzone="data" class="rounded-lg m-4 w-64 col center p-4 bg-gray-500 gap-4">
            <Icon icon="mdi-lightning-bolt" class="x2  text-accent" />
            <p class="text-center text-xs font-sans">Drop Function Definitions Here</p>
          </div>
        <BtnGradient text="Create Assistant" type="submit" class="my-6 text-center" />
      </form>
    </section>
  </aside>
</template>