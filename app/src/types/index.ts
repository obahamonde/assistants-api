// Assistant
type AssistantResponse = {
  id: string;
  avatar: string;
  created_at: number;
  description?: string;
  file_ids: string[];
  instructions?: string;
  metadata?: any;
  model: string;
  name?: string;
  object: "assistant";
  tools: Array<ToolCodeInterpreter | ToolRetrieval | ToolFunction>;
};

type ToolCodeInterpreter = {
  type: "code_interpreter";
};

type ToolRetrieval = {
  type: "retrieval";
};

type ToolFunction = {
  function: FunctionDefinition;
  type: "function";
};

type FunctionProperty = {
  title?: string;
  type?: string;
  description?: string;
  default?: string;
};

type FunctionParameters = {
  type: "object";
  properties: {
    [key: string]: FunctionProperty;
  };
  required?: string[];
};

type FunctionDefinition = {
  name: string;
  parameters: FunctionParameters;
  description: string;
};

// Thread
type ThreadResponse = {
  id: string;
  created_at: number;
  metadata?: any;
  object: "thread";
  title: string;
};

// Run
type RunResponse = {
  id: string;
  assistant_id: string;
  cancelled_at?: number;
  completed_at?: number;
  created_at: number;
  expires_at: number;
  failed_at?: number;
  file_ids: string[];
  instructions: string;
  last_error?: LastError;
  metadata?: any;
  model: string;
  object: "thread.run";
  required_action?: RequiredAction;
  started_at?: number;
  status:
    | "queued"
    | "in_progress"
    | "requires_action"
    | "cancelling"
    | "cancelled"
    | "failed"
    | "completed"
    | "expired";
  thread_id: string;
  tools: Array<
    | ToolAssistantToolsCode
    | ToolAssistantToolsRetrieval
    | ToolAssistantToolsFunction
  >;
};

type ToolAssistantToolsCode = {
  type: "code_interpreter";
};

type ToolAssistantToolsRetrieval = {
  type: "retrieval";
};

type ToolAssistantToolsFunction = {
  function: FunctionDefinition;
  type: "function";
};

type LastError = {
  code: "server_error" | "rate_limit_exceeded";
  message: string;
};

type RequiredAction = {
  submit_tool_outputs: RequiredActionSubmitToolOutputs;
  type: "submit_tool_outputs";
};

type RequiredActionSubmitToolOutputs = {
  tool_calls: Array<RequiredActionFunctionToolCall>;
};

type RequiredActionFunctionToolCall = {
  id: string;
  function: TFunction;
  type: "function";
};

// Function (redefined for RequiredActionFunctionToolCall)
type TFunction = {
  arguments: string;
  name: string;
};

// ThreadMessage
type ThreadMessageResponse = {
  id: string;
  assistant_id: string;
  content: MessageContentText[];
  created_at: number;
  file_ids: string[];
  metadata?: any;
  object: "thread.message";
  role: "user" | "assistant";
  run_id: string;
  thread_id: string;
};

type MessageContentText = {
  text: TText;
  type: "text";
};

type TText = {
  annotations: TextAnnotationFileCitation[] | TextAnnotationFilePath[];
  value: string;
};

type TextAnnotationFileCitation = {
  end_index: number;
  file_citation: TextAnnotationFileCitationFileCitation;
  start_index: number;
  text: string;
  type: "file_citation";
};

type TextAnnotationFilePath = {
  end_index: number;
  file_path: TextAnnotationFilePathFilePath;
  start_index: number;
  text: string;
  type: "file_path";
};

type TextAnnotationFileCitationFileCitation = {
  file_id: string;
  quote: string;
};

type TextAnnotationFilePathFilePath = {
  file_id: string;
};

// FileObject
type FileObjectResponse = {
  id: string;
  bytes: number;
  url: string;
  created_at: number;
  filename: string;
  object: "file";
  purpose:
    | "fine-tune"
    | "fine-tune-results"
    | "assistants"
    | "assistants_output";
  status: "uploaded" | "processed" | "error";
  status_details: string;
};

// CodeToolCall
type CodeToolCall = {
  id: string;
  code_interpreter: CodeInterpreter;
  type: "code_interpreter";
};

type CodeInterpreter = {
  input: string;
  outputs: Array<CodeInterpreterOutputLogs | CodeInterpreterOutputImage>;
};

type CodeInterpreterOutputLogs = {
  logs: string;
  type: "logs";
};

type CodeInterpreterOutputImage = {
  image: CodeInterpreterOutputImageImage;
  type: "image";
};

type CodeInterpreterOutputImageImage = {
  file_id: string;
};

// MessageCreationStepDetails
type MessageCreationStepDetails = {
  message_creation: MessageCreation;
  type: "message_creation";
};

type MessageCreation = {
  message_id: string;
};

// ToolCallsStepDetails
type ToolCallsStepDetails = {
  tool_calls: Array<CodeToolCall | RetrievalToolCall | FunctionToolCall>;
  type: "tool_calls";
};

type RetrievalToolCall = {
  id: string;
  retrieval: any; // Type not defined in JSON schema
  type: "retrieval";
};

type FunctionToolCall = {
  id: string;
  function: TFunction;
  type: "function";
};

type AssistantRequest = {
  model: "gpt-4-1106-preview" | "gpt-3.5-turbo-0613"; // The model to use for the assistant
  description?: string; // Description of the assistant
  file_ids: string[]; // File IDs to use for the assistant
  name: string; // Name of the assistant
  instructions: string; // Instructions for the assistant
  tools: Array<
    | ToolAssistantToolsFunction
    | ToolAssistantToolsCode
    | ToolAssistantToolsRetrieval
  >; // The tools to use for the assistant
};

type FileObjectRequest = {
  file: File; // The file to upload
};

type ThreadMessageRequest = {
  thread_id: string; // The thread ID of the thread to use for the thread message
  content: string; // The content of the thread message
  role?: "user"; // The role of the thread message (optional, default: "user")
  file_ids?: string[]; // The file IDs of the thread message (optional)
};

type ThreadRequest = {
  messages: Message[]; // The messages to use for the thread
};

// Message Type
type Message = {
  content: string; // The content of the message
  role: "user" | "assistant"; // The role of the message
  file_ids?: string[]; // File IDs associated with the message (optional)
  // Add additional properties for the message if they exist
};

type RunRequest = {
  assistant_id: string; // The assistant ID of the assistant to use for the run
  thread_id: string; // The thread ID of the thread to use for the run
  tools?: Array<
    | ToolAssistantToolsFunction
    | ToolAssistantToolsCode
    | ToolAssistantToolsRetrieval
  >; // The tools to use for the run
};

type GoogleUserInfo = {
  id: string;
  name: string;
  givenName: string;
  familyName: string;
  picture: string;
  locale: string;
};

export type {
  AssistantResponse,
  ThreadResponse,
  RunResponse,
  ThreadMessageResponse,
  FileObjectResponse,
  CodeToolCall,
  MessageCreationStepDetails,
  ToolCallsStepDetails,
  ToolFunction,
  AssistantRequest,
  FileObjectRequest,
  ThreadMessageRequest,
  ThreadRequest,
  Message,
  RunRequest,
  GoogleUserInfo,
  ToolAssistantToolsFunction,
  FunctionDefinition,
};
