import TextRendererCard from "./textRendererCard";

interface TextRendererBoxProps {
  prompt: string;
  response: string;
}

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
    <div className="flex justify-center w-full">
      <div className="lg:text-2xl sm:text-xl font-medium">
        How can I help you ?
      </div>
    </div>
  );
}

export default function TextRendererBox(props: TextRendererBoxProps) {
  return (
    <div className="flex h-4/6 flex-col items-start justify-center max-w-100% w-full overflow-y-scroll ">
      <RenderText promptToRender={props.prompt} data={props.response} />
    </div>
  );
}
