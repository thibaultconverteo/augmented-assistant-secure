import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ButtonLoading } from "@/components/ui/button-loading";

import { ArrowUpIcon } from "@radix-ui/react-icons";
import React, { useState } from "react";
import { useWindowSize } from "react-use";
import { twMerge } from "tailwind-merge";
import ButtonDelete from "@/components/ui/button-delete";

interface TextAreaFormProps {
  onTextSubmit: (text: string) => void;
  isloading: boolean;
}

const ResizableTextArea: React.FC<{
  inputValue: string;
  handleChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleKeyDown: (event: React.KeyboardEvent<HTMLTextAreaElement>) => void;
}> = ({ inputValue, handleChange, handleKeyDown }) => {
  return (
    <Textarea
      value={inputValue}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      placeholder="Type something..."
      className="flex min-h-10 max-h-96 w-full resize-none md:w-[400px] lg:w-[500px] xl:w-[600px] 2xl:w-[700px] "
      style={{
        height: `calc(1em + ${inputValue.split("\n").length * 1.2}em)`,
        maxHeight: "20em",
      }}
    ></Textarea>
  );
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

  if (typeof window !== "undefined") {
    if (sessionStorage.chat_history) {
    }
  }

  const handleTextareaKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      const formEvent = new Event("submit", { bubbles: true });
      event.currentTarget.form?.dispatchEvent(formEvent);
    }
  };

  return (
    <div className="w-full flex justify-center items-center absolute bottom-1 space-x-2">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-[1fr_auto] gap-2 justify-center items-center w-full">
          <ResizableTextArea
            inputValue={inputValue}
            handleChange={handleChange}
            handleKeyDown={handleTextareaKeyDown}
          />

          {props.isloading ? (
            <ButtonLoading />
          ) : (
            <Button type="submit" size={width > 767 ? "default" : "icon"}>
              <ArrowUpIcon
                className={twMerge(width > 767 && "mr-2", "h-5 w-5")}
              />
              {width > 767 && "Send message"}
            </Button>
          )}
        </div>
      </form>

      <ButtonDelete />
    </div>
  );
}
