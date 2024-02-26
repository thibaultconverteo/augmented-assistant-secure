import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon } from "@radix-ui/react-icons";
import React, { useState } from "react";

interface TextAreaFormProps {
  onTextSubmit: (text: string) => void;
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

export default function TextAreaForm(props: TextAreaFormProps) {
  const [inputValue, setInputValue] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    props.onTextSubmit(inputValue);
    setInputValue("");
  };

  return (
    <div className="w-full flex justify-center absolute bottom-1 ">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-[1fr_auto] gap-2 justify-center items-center w-full">
          <ResizableTextArea
            inputValue={inputValue}
            handleChange={handleChange}
          />

          <Button type="submit" size="icon">
            <ArrowUpIcon className="h-5 w-5" />
          </Button>
        </div>
      </form>
    </div>
  );
}
