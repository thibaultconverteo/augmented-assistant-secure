"use server";
import logger from "@/lib/logger";

let session_id = "";
const url = {
  general:
    "https://analytics-assistant-backend-4o52ykz34a-ew.a.run.app/processPrompt",
  ga: "https://augmented-chatbot-demo-anonimized-4o52ykz34a-ew.a.run.app/processPrompt",
};
const key = "sessionId";

export async function getData(
  prompt: string | undefined,
  chatHistory: string | null,
  ai_model: string | null,
  agentId: string | null
) {
  const cleanedAiModel = ai_model?.replace(/['"]+/g, "");
  const selectedUrl = url[cleanedAiModel as keyof typeof url];

  logger.info(`user prompt: ${prompt}`);
  if (session_id !== "") {
    logger.info(`session id: ${session_id}`);
  }

  if (chatHistory === null) {
    const getFirstApiResponseStart = Date.now();

    const res = await fetch(selectedUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(agentId !== null && { agentId: agentId }),
      },
      body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
    });

    const data = await res.json();
    const getFirstApiResponseEnd = Date.now();
    const getFirstApiResponse =
      getFirstApiResponseEnd - getFirstApiResponseStart;
    logger.info(`first api response time: ${getFirstApiResponse}ms`);

    session_id = data.sessionId;

    delete data[key];

    return data;
  }

  const getApiResponseStart = Date.now();
  const res = await fetch(selectedUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      sessionId: session_id,
      ...(agentId !== null && { agentId: agentId }),
    },
    body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
  });

  const data = await res.json();
  const getApiResponseEnd = Date.now();
  const getApiResponse = getApiResponseEnd - getApiResponseStart;
  logger.info(`api response time: ${getApiResponse}ms`);

  delete data[key];

  return data;
}
