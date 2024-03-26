interface IframeProps {
  source: string;
}

export default function TextRendererItemIframe(props: IframeProps) {
  const encodeResponse = encodeURIComponent(props.source || "");

  return (
    <iframe
      src={"data:text/html;charset=utf-8," + `${encodeResponse}`}
      className="w-10/12 xl:w-[130vh] lg:w-[100vh] md:w-full sm:w-[50vh] h-full xl:h-[60vh] lg:h-[35vh] md:h-[30vh] sm:h-[25vh]"
      id="chartIframe"
    />
  );
}
