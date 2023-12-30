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
const show = ref<boolean>(false);
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
const deleteAssistant = async (assistant: AssistantResponse) => {
  await del(`${url}/${assistant.id}?user=${key}`, undefined, {
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
    <section class="flex-1 p-4" v-if="!show">
    <div class="row center" v-if="state.currentAssistant">
      <Icon icon="mdi-chevron-left" @click="index--" class="scale-200 cp" v-if="!loading" />
      <AppAssistant :current-assistant="currentAssistant" :handle-click="deleteAssistant"  :index="index"/>
      <Icon icon="mdi-chevron-right" @click="index++" class="scale-200 cp" v-if="!loading"  />
    </div>
      <FunctionCatalogue :assistant="assistantRequest"/>
     </section>
   
    <section class="flex-1 p-4" v-if="show">
      <form @submit.prevent="postAssistant(assistantRequest)" class="col center p-4">
        <InputFormField name="Name" @change="assistantRequest.name = $event" />
        <InputTextAreaField
          name="Description"
          @change="assistantRequest.description = $event" />
        <InputTextAreaField
          name="Instructions"
          @change="assistantRequest.instructions = $event" />
        
        <BtnGradient text="Create Assistant" type="submit" class="my-6 text-center" />
      </form>
    </section> <BtnGradient :text="show ? 'Show Tools':'Configure Assistant'" @click="show = !show" class="my-6 text-center" /></aside>
</template>