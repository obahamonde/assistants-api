import {
  ToolAssistantToolsFunction,
  FunctionDefinition,
  AssistantRequest,
} from "~/types";

export const useFunctions = () => {
  const getFunctionCatalog = async () => {
    const response = await useFetch("/api/function", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).json<FunctionDefinition[]>();
    if (response.data) {
      return response.data;
    }
    throw new Error("No data");
  };
  const runFunction = async <T>(text: string) => {
    const response = await useFetch(`/api/function?text=${text}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }).json<T>();
    if (response.data) {
      return response.data;
    }
    throw new Error("No data");
  };
  const attachFunction = (
    assistantRequest: AssistantRequest,
    functionDefinition: FunctionDefinition,
  ) => {
    assistantRequest.tools.push({
      type: "function",
      function: functionDefinition,
    } as ToolAssistantToolsFunction);
  };
  return { getFunctionCatalog, runFunction, attachFunction };
};
