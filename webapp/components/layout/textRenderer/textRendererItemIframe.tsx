interface IframeProps {
  source: string;
}

export default function TextRendererItemIframe(props: IframeProps) {
  const encodeResponse = encodeURIComponent(props.source || "");

  return (
    <iframe
      src={"data:text/html;charset=utf-8," + `${encodeResponse}`}
      className="w-10/12 xl:w-[130vh] lg:w-[100vh] md:w-full h-full lg:h-[32em] md:h-[30em] sm:h-[25em]"
      id="chartIframe"
    />
  );
}
