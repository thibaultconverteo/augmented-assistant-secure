import TextRendererItem from "./textRendererItem";

interface TextRendererCardProps {
  data: string;
  prompt: string;
}

export default function TextRendererCard(props: TextRendererCardProps) {
  return (
    <div className="flex h-full flex-col items-start justify-center max-w-100% gap-10">
      <TextRendererItem text={props.prompt} user="user" />
      <TextRendererItem text={props.data} user="chatbot" />
    </div>
  );
}
