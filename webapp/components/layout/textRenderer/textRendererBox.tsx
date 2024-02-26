import data from "../../../data/test.json";
import TextRendererCard from "./textRendererCard";

interface TextRendererBoxProps {
  prompt: string;
  response: string;
}

let random = Math.floor(Math.random() * 2);

function RenderText({
  promptToRender,
  data,
}: {
  promptToRender: string;
  data: string;
}) {
  if (promptToRender) {
    return <TextRendererCard prompt={promptToRender} data={data} />;
  }

  return (
    <div className=" lg:text-2xl sm:text-xl font-medium">
      How can I help you ?
    </div>
  );
}

export default function TextRendererBox(props: TextRendererBoxProps) {
  return (
    <div className="flex h-full flex-col items-center justify-center max-w-100%">
      <RenderText promptToRender={props.prompt} data={props.response} />
    </div>
  );
}
