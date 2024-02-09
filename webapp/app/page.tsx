"use client";
import TextAreaForm from "@/components/layout/textAreaForm";
import TextRendererBox from "@/components/layout/textRendererBox";
import React, { useState } from "react";

export default function Home() {
  const [displayValue, setDisplayValue] = useState("");

  const handleTextSubmit = (text: string) => {
    setDisplayValue(text);
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-2">
      <TextRendererBox text={displayValue} />
      <TextAreaForm onTextSubmit={handleTextSubmit} />
    </div>
  );
}
