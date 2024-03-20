let session_id = "";
const url =
  "https://augmented-chatbot-demo-4o52ykz34a-ew.a.run.app/processPrompt";

export async function getData(prompt: string | undefined) {
  const chatHistory = sessionStorage.getItem("chat_history");
  if (chatHistory === null) {
    const res = await fetch(
      url,

      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
      }
    );

    const data = await res.json();
    session_id = data.sessionId;

    return data;
  }

  const res = await fetch(
    url,

    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        sessionId: session_id,
      },
      body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
    }
  );

  const data = await res.json();

  const key = "sessionId";

  delete data[key];

  return data;
}
