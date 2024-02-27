export async function getData(prompt: string | undefined) {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_URL + "/processPrompt",

    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt?.toLowerCase() }),
    }
  );

  const data = await res.json();
  return data.response;
}
