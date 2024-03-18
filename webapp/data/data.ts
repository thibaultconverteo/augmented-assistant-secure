let sessionId = "";

export async function getData(prompt: string | undefined) {
  const chatHistory = localStorage.getItem("chat_history");
  if (chatHistory === null) {
    const res = await fetch(
      "https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app/processPrompt",

      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
      }
    );

    const data = await res.json();
    sessionId = data.sessionId;

    return data;
  }

  const res = await fetch(
    "https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app/processPrompt",

    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        sessionId: "sessionId",
      },
      body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
    }
  );

  const data = await res.json();
  const key = "sessionId";
  delete data[key];

  return data;
}
