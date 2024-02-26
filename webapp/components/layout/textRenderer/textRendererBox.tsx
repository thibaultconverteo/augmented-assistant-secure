import data from "../../../data/test.json";
import TextRendererCard from "./textRendererCard";

interface TextRendererBoxProps {
  prompt: string;
}

function RenderText({ promptToRender }: { promptToRender: string }) {
  if (promptToRender) {
    let random = Math.floor(Math.random() * 9);
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
    <div className="flex h-4/6 flex-col items-start justify-center max-w-100% w-full overflow-y-scroll ">
      <RenderText promptToRender={props.prompt} />
    </div>
  );
}
