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
  return (
    <div className=" space-x-10">
      <div className="flex space-x-4">
        <p>{userIcon[props.user]}</p>
        {UserName(props)}
      </div>
      <div dangerouslySetInnerHTML={{ __html: props.text }} />
    </div>
  );
}
