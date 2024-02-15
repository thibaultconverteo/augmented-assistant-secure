import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon } from "@radix-ui/react-icons";
import React, { SetStateAction, useState } from "react";

interface TextAreaFormProps {
  onTextSubmit: (text: string) => void;
}

export default function TextAreaForm(props: TextAreaFormProps) {
  const [inputValue, setInputValue] = useState("");

  const handleChange = (e: { target: { value: SetStateAction<string> } }) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    props.onTextSubmit(inputValue);
    setInputValue("");
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-[1fr_auto] gap-2 justify-center items-center">
          <Textarea
            value={inputValue}
            onChange={handleChange}
            placeholder="Type something..."
            className="flex min-h-10 max-h-96 resize-none w-full "
          ></Textarea>

          <Button type="submit" size="icon">
            <ArrowUpIcon className="h-5 w-5" />
          </Button>
        </div>
      </form>
    </div>
  );
}
