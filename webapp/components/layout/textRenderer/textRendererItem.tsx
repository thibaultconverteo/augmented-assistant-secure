import React from "react";

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
        localStorage.getItem("chat_history") || "[]"
      );
      const isMessageDuplicate = storedMessages.some(
        (message: any) =>
          message.data.response === props.response.response &&
          message.user === props.user
      );
      if (!isMessageDuplicate) {
        const updatedMessages = [
          ...storedMessages,
          { data: props.response, user: props.user },
        ];
        localStorage.setItem("chat_history", JSON.stringify(updatedMessages));
      }
    }
  }, [props.response, props.user]);

  const encodeResponse = encodeURIComponent(props.response?.response || "");

  return (
    <div className="space-x-10">
      <div className="flex space-x-4">
        <p>{userIcon[props.user]}</p>
        {UserName(props)}
      </div>
      {props.response?.type === "html" ? (
        <iframe
          src={"data:text/html;charset=utf-8," + `${encodeResponse}`}
          className="w-10/12 lg:h-[33em] md:h-[30em] sm:h-[20em]  overflow-auto"
          id="chartIframe"
        />
      ) : (
        <div className="whitespace-pre-wrap break-words">
          {props.response?.response}
        </div>
      )}
    </div>
  );
}
