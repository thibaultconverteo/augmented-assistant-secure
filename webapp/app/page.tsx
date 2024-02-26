"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRenderer/textRendererBox";
import React, { useState } from "react";
import { getData } from "@/data/data";

export default function Home() {
  const [promptValue, setPromptValue] = useState("");
  const [apiResponse, setApiResponse] = useState("");

  const handleTextSubmit = (text: string) => {
    setPromptValue(text);
    getData(text).then((data) => {
      console.log(data);
      setApiResponse(data);
    });
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-2">
      <TextRendererBox prompt={promptValue} response={apiResponse} />
      <TextAreaForm onTextSubmit={handleTextSubmit} />
    </div>
  );
}
