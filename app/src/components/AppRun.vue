<script setup lang="ts">
import { useRun } from "../composables/run";
import useStore from "../store";
const { state } = useStore();
const { startRun, eventListener } = useRun();
const execRun = async () => {
  if (!state.currentThread) {
    alert("Please select a thread");
    return;
  }
  if (!state.currentAssistant) {
    alert("Please select an assistant");
    return;
  }
  const run = await startRun(state.currentThread.id, state.currentAssistant.id);
  eventListener(state.currentThread.id, run.id, (event) => {
    state.messages.push(event);
  });
  3;
  return run;
};
</script>
<template>
  <div class="row center gap-4">
    <slot :exec="execRun" />
  </div>
</template>
