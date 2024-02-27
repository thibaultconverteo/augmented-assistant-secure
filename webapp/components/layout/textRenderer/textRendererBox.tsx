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
    <div className="flex justify-center w-full relative top-1/2 ">
      <div className="lg:text-2xl sm:text-xl font-medium">
        How can I help you ?
      </div>
    </div>
  );
}

export default function TextRendererBox(props: TextRendererBoxProps) {
  return (
    <div className="flex h-5/6 mt-0 flex-col items-start justify-start max-w-100% w-full overflow-y-auto">
      <RenderText promptToRender={props.prompt} data={props.response} />
    </div>
  );
}
