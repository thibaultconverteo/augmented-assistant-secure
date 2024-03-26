import React from "react";
import { Skeleton } from "@/components/ui/skeleton";
import TextRendererItemIframe from "./textRendererItemIframe";

interface TextRendererItemProps {
  response: { response: string; type: string };
  user: "chatbot" | "user";
}

const userIcon = {
  chatbot: "🤖",
  user: "🙂",
};

function UserName(props: TextRendererItemProps) {
  if (props.user === "chatbot") {
    return <p className="text-xl font-semibold">Chatbot</p>;
  }
  return <p className="text-xl font-semibold">You</p>;
}

export default function TextRendererItem(props: TextRendererItemProps) {
  React.useEffect(() => {
    if (props.response?.response && props.response?.response.trim() !== "") {
      const storedMessages = JSON.parse(
        sessionStorage.getItem("chat_history") || "[]"
      );
      const isMessageDuplicate = storedMessages.some(
        (message: any) =>
          message.text.response === props.response.response &&
          message.user === props.user
      );
      if (!isMessageDuplicate) {
        const updatedMessages = [
          ...storedMessages,
          { text: props.response, user: props.user },
        ];
        sessionStorage.setItem("chat_history", JSON.stringify(updatedMessages));
      }
    }
  }, [props.response, props.user]);

  return (
    <div className="space-x-10">
      <div className="flex space-x-4">
        <p>{userIcon[props.user]}</p>
        {UserName(props)}
      </div>
      {props.response?.type === "html" ? (
        <TextRendererItemIframe source={props.response?.response} />
      ) : props.response?.response === "..." ? (
        <div className="flex items-center space-x-4">
          <div className="space-y-2">
            <Skeleton className="h-4 w-[400px] bg-gray-200 dark:bg-zinc-700" />
            <Skeleton className="h-4 w-[400px] bg-gray-200 dark:bg-zinc-700" />
            <Skeleton className="h-4 w-[400px] bg-gray-200 dark:bg-zinc-700" />
            <Skeleton className="h-4 w-[250px] bg-gray-200 dark:bg-zinc-700" />
          </div>
        </div>
      ) : (
        <div className="whitespace-pre-wrap break-words">
          {props.response?.response}
        </div>
      )}
    </div>
  );
}
