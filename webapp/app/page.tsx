"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRenderer/textRendererBox";
import React, { useState } from "react";
import { getData } from "@/data/data";

export default function Home() {
  const [promptValue, setPromptValue] = useState("");
  const [apiResponse, setApiResponse] = useState("");
  const [isloading, setIsLoading] = useState(false);

  const handleTextSubmit = (text: string) => {
    setIsLoading(true);
    getData(text).then((data) => {
      setPromptValue(text);
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
