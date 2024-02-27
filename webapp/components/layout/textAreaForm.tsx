import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon, TrashIcon } from "@radix-ui/react-icons";
import React, { useState } from "react";
import { ButtonLoading } from "../ui/button-loading";
import { useWindowSize } from "react-use";
import { twMerge } from "tailwind-merge";

interface TextAreaFormProps {
  onTextSubmit: (text: string) => void;
  isloading: boolean;
}

const ResizableTextArea: React.FC<{
  inputValue: string;
  handleChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
}> = ({ inputValue, handleChange }) => {
  return (
    <Textarea
      value={inputValue}
      onChange={handleChange}
      placeholder="Type something..."
      className="flex min-h-10 max-h-96 w-full resize-none md:w-[400px] lg:w-[500px] xl:w-[600px] 2xl:w-[700px] "
      style={{
        height: `calc(1em + ${inputValue.split("\n").length * 1.2}em)`,
        maxHeight: "20em",
      }}
    ></Textarea>
  );
};

const clearLocalStorage = () => {
  localStorage.removeItem("chat_history");
};

export default function TextAreaForm(props: TextAreaFormProps) {
  const [inputValue, setInputValue] = useState("");
  const { width } = useWindowSize();

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    props.onTextSubmit(inputValue);
    setInputValue("");
  };

  return (
    <div className="w-full flex justify-center items-center absolute bottom-1 space-x-2">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-[1fr_auto] gap-2 justify-center items-center w-full">
          <ResizableTextArea
            inputValue={inputValue}
            handleChange={handleChange}
          />

          {props.isloading ? (
            <ButtonLoading />
          ) : (
            <Button type="submit" size="icon">
              <ArrowUpIcon className="h-5 w-5" />
            </Button>
          )}
        </div>
      </form>
      <Button
        variant="destructive"
        onClick={clearLocalStorage}
        className="h-10"
        size={width > 767 ? "default" : "icon"}
      >
        <TrashIcon className={twMerge(width > 767 && "mr-2", "h-5 w-5")} />
        {width > 767 && "Delete history "}
      </Button>
    </div>
  );
}
