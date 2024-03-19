import React, { useEffect, useState } from "react";
import TextRendererItem from "./textRendererItem";

interface Message {
  text: { response: string; type: string };
  user: "chatbot" | "user";
}

interface TextRendererCardProps {
  data: { response: string; type: string };
  prompt: { response: string; type: string };
}

export default function TextRendererCard(props: TextRendererCardProps) {
  const [chatHistory, setChatHistory] = useState<Message[]>([]);

  useEffect(() => {
    fetchChatHistory();
  }, [props.data, props.prompt]);

  const fetchChatHistory = () => {
    const storedHistory = localStorage.getItem("chat_history");
    if (storedHistory) {
      setChatHistory(JSON.parse(storedHistory));
    }
  };

  return (
    <div className="grid grid-cols items-start justify-center max-w-100% gap-10">
      {chatHistory.map((message, index) => (
        <TextRendererItem
          key={index}
          response={message.text}
          user={message.user}
        />
      ))}
      <div className="hidden">
        <TextRendererItem response={props.prompt} user="user" />
        <TextRendererItem response={props.data} user="chatbot" />
      </div>
    </div>
  );
}
