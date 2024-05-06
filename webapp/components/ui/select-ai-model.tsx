"use client";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useWindowSize } from "react-use";
import { useSessionStorage } from "react-use";

export default function SelectAiModel() {
  const { width } = useWindowSize();
  const [model, setModel] = useSessionStorage("ai_model", "general");

  const handleModelChange = (value: string) => {
    setModel(value);
  };

  return (
    <Select defaultValue={model} onValueChange={handleModelChange}>
      <SelectTrigger className="w-auto gap-1">
        {width > 767 && <span>Model:</span>}
        {width > 767 && <SelectValue />}
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="general">General</SelectItem>
        <SelectItem value="ga">GA</SelectItem>
      </SelectContent>
    </Select>
  );
}
