<script setup lang="ts">
import useStore from "~/store";
import type { ThreadMessageResponse, GoogleUserInfo } from "~/types";
const props = defineProps<{
  user: GoogleUserInfo;
}>();
const get = useRequest<undefined, ThreadMessageResponse[]>();
const { state } = useStore();
const getMessages = async () => {
  if (!state.currentThread) return;
  const { data } = await get(
    `/api/thread_messages?user=${props.user.id}`,
    undefined,
    {
      headers: {
        "Content-Type": "application/json",
      },
    },
  );
  if (!data.value) return;
  state.messages = data.value.filter(
    (message) => message.thread_id === state.currentThread?.id,
  );
};
onMounted(async () => {
  await getMessages();
});
watch(
  () => state.currentThread,
  async () => {
    await getMessages();
  },
);
</script>
<template>
  <section class="col start">
    <ul class="col start gap-4" v-if="state.currentAssistant" >
     <AppMessage v-for="message in state.messages" :message="message" :assistant="state.currentAssistant" :user="props.user" />
    </ul>

  </section>
</template>
<style scoped>
/* Estilos existentes... */

/* Alinear los elementos al final (derecha) */
.end {
  align-self: flex-end;
  text-align: right;
}

/* Alinear los elementos al inicio (izquierda) */
.start {
  align-self: flex-start;
  text-align: left;
}

/* Estilos para los mensajes */
li {
  display: flex;
  flex-direction: column;
}

/* Estilos para los bloques de mensajes */
.row {
  display: flex;
  flex-direction: row;
  align-items: center; /* Alinea los ítems (imagen y texto) verticalmente */
}

/* Estilos para las imágenes de perfil */
img.w-8.h-8.rounded-full.m-4 {
  border-radius: 50%; /* Hace que las imágenes sean circulares */
  margin: 4px; /* Espaciado alrededor de la imagen */
  width: 32px; /* Ancho de la imagen */
  height: 32px; /* Altura de la imagen */
}


</style>
