"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRenderer/textRendererBox";
import React, { useState } from "react";
import { getData } from "@/data/data";

export default function Home() {
  const [promptValue, setPromptValue] = useState<{
    response: string;
    type: string;
  }>({ response: "", type: "" });
  const [isloading, setIsLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<{
    response: string;
    type: string;
  }>({ response: "", type: "" });

  const handleTextSubmit = (text: string) => {
    setIsLoading(true);
    setPromptValue({ response: text, type: "text" });
    setApiResponse({ response: "...", type: "text" });

    getData(text).then((data: { response: string; type: string }) => {
      sessionStorage.chat_history = JSON.stringify(
        JSON.parse(sessionStorage.chat_history ?? "[]").slice(0, -1)
      );
      setApiResponse(data);
      setIsLoading(false);
    });
  };

  return (
    <div className="w-full h-full flex flex-col items-center p-2 gap-y-10">
      <TextRendererBox prompt={promptValue} response={apiResponse} />
      <TextAreaForm onTextSubmit={handleTextSubmit} isloading={isloading} />
    </div>
  );
}
