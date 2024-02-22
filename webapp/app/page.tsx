"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRenderer/textRendererBox";
import React, { useState } from "react";

export default function Home() {
  const [promptValue, setPromptValue] = useState("");

  const handleTextSubmit = (text: string) => {
    setPromptValue(text);
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-2">
      <TextRendererBox prompt={promptValue} />
      <TextAreaForm onTextSubmit={handleTextSubmit} />
    </div>
  );
}
