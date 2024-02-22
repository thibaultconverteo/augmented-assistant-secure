import data from "../../../data/test.json";
import TextRendererCard from "./textRendererCard";

interface TextRendererBoxProps {
  prompt: string;
}

let random = Math.floor(Math.random() * 2);

function RenderText({ promptToRender }: { promptToRender: string }) {
  if (promptToRender) {
    let random = Math.floor(Math.random() * 2);
    const content = data[random].content;
    return <TextRendererCard prompt={promptToRender} data={content} />;
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
      <RenderText promptToRender={props.prompt} />
    </div>
  );
}
