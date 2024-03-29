let session_id = "";
const url = {
  general:
    "https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app/processPrompt",
  ga: "",
};
const key = "sessionId";

export async function getData(prompt: string | undefined) {
  const chatHistory = sessionStorage.getItem("chat_history");
  const ai_model = sessionStorage.getItem("ai_model");
  const cleanedAiModel = ai_model?.replace(/['"]+/g, "");

  const selectedUrl = url[cleanedAiModel as keyof typeof url];

  if (chatHistory === null) {
    const res = await fetch(selectedUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
    });

    const data = await res.json();
    session_id = data.sessionId;

    delete data[key];

    return data;
  }

  const res = await fetch(selectedUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      sessionId: session_id,
    },
    body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
  });

  const data = await res.json();

  delete data[key];

  return data;
}
