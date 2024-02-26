export async function getData(prompt: string | undefined) {
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
  return data;
}
