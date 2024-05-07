"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRenderer/textRendererBox";
import React, { useState, useTransition } from "react";
import { getData } from "@/data/data";
import { useSearchParams } from "next/navigation";

export default function Home() {
  const [promptValue, setPromptValue] = useState<{
    response: string;
    type: string;
  }>({ response: "", type: "" });
  const [apiResponse, setApiResponse] = useState<{
    response: string;
    type: string;
  }>({ response: "", type: "" });

  const [isloading, startTransition] = useTransition();

  const searchParams = useSearchParams();

  const agentId = searchParams.get("agentId");
  console.log("agent id ", agentId);

  const handleTextSubmit = (text: string) => {
    setPromptValue({ response: text, type: "text" });
    setApiResponse({ response: "...", type: "text" });
    const chatHistory = sessionStorage.getItem("chat_history");
    const ai_model = sessionStorage.getItem("ai_model");

    startTransition(() => {
      getData(text, chatHistory, ai_model, agentId).then(
        (data: { response: string; type: string }) => {
          sessionStorage.chat_history = JSON.stringify(
            JSON.parse(sessionStorage.chat_history ?? "[]").slice(0, -1)
          );
          setApiResponse(data);
        }
      );
    });
  };

  return (
    <div className="w-full h-full flex flex-col items-center p-2 gap-y-10">
      <TextRendererBox prompt={promptValue} response={apiResponse} />
      <TextAreaForm onTextSubmit={handleTextSubmit} isloading={isloading} />
    </div>
  );
}
