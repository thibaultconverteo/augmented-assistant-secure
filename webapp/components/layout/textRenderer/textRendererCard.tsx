import React, { useEffect, useState } from "react";
import TextRendererItem from "./textRendererItem";

interface Message {
  text: string;
  user: "chatbot" | "user";
}

interface TextRendererCardProps {
  data: string;
  prompt: string;
}

export default function TextRendererCard(props: TextRendererCardProps) {
  // Retrieve chat history from local storage
  const [chatHistory, setChatHistory] = useState<Message[]>([]);

  useEffect(() => {
    fetchChatHistory();
  }, [props.data, props.prompt]); // Fetch chat history when data or prompt changes

  const fetchChatHistory = () => {
    const storedHistory = localStorage.getItem("chat_history");
    if (storedHistory) {
      setChatHistory(JSON.parse(storedHistory));
    }
  };

  return (
    <div className="grid grid-cols items-start justify-center max-w-100% gap-10 h-full">
      {chatHistory.map((message, index) => (
        <TextRendererItem key={index} text={message.text} user={message.user} />
      ))}
      <div className=" hidden">
        <TextRendererItem text={props.prompt} user="user" />

        <TextRendererItem text={props.data} user="chatbot" />
      </div>
    </div>
  );
}
