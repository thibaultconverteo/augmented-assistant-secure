interface TextRendererBoxProps {
  text: string;
}

function RenderText({ textToRender }: { textToRender: string }) {
  if (textToRender) {
    return <p>{textToRender}</p>;
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
      <RenderText textToRender={props.text} />
    </div>
  );
}
