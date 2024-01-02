import { RunResponse, ThreadMessageResponse } from "~/types";

export const useRun = () => {
  async function startRun(thread_id: string, assistant_id: string) {
    const { data } = await useFetch(
      `/api/run/${thread_id}?assistant_id=${assistant_id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      },
    ).json<RunResponse>();
    if (data.value) {
      return data.value;
    }
    throw new Error("No data");
  }

  async function eventListener(
    thread_id: string,
    run_id: string,
    callback: (eventData: ThreadMessageResponse) => any,
  ) {
    const eventSource = new EventSource(
      `/api/run/${thread_id}?run_id=${run_id}`,
    );
    eventSource.addEventListener("done", (event) => {
      eventSource.close();
    });
    eventSource.addEventListener("message", (event) => {
      callback(JSON.parse(event.data));
    });
  }

  return { startRun, eventListener };
};
