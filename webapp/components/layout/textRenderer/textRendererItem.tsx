// textRendererItem.tsx
import React from "react";

interface TextRendererItemProps {
  text: string;
  user: "chatbot" | "user";
}

const userIcon = {
  chatbot: "🤖",
  user: "👤",
};

function UserName(props: TextRendererItemProps) {
  if (props.user === "chatbot") {
    return <p className="text-xl font-semibold">Chatbot</p>;
  }
  return <p className="text-xl font-semibold">You</p>;
}

export default function TextRendererItem(props: TextRendererItemProps) {
  // Save message to local storage
  React.useEffect(() => {
    const storedMessages = JSON.parse(
      localStorage.getItem("chat_history") || "[]"
    );
    const isMessageDuplicate = storedMessages.some(
      (message: any) =>
        message.text === props.text && message.user === props.user
    );
    if (!isMessageDuplicate) {
      const updatedMessages = [
        ...storedMessages,
        { text: props.text, user: props.user },
      ];
      localStorage.setItem("chat_history", JSON.stringify(updatedMessages));
    }
  }, [props.text, props.user]);

  return (
    <div className=" space-x-10">
      <div className="flex space-x-4">
        <p>{userIcon[props.user]}</p>
        {UserName(props)}
      </div>
      <div
        dangerouslySetInnerHTML={{ __html: props.text }}
        className="whitespace-pre-wrap break-words"
      />
    </div>
  );
}
