"use client";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useWindowSize } from "react-use";

export default function SelectAiModel() {
  const { width } = useWindowSize();

  return (
    <Select defaultValue="general">
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
