import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function SelectAiModel() {
  return (
    <Select defaultValue="general">
      <SelectTrigger className="w-[160px]">
        <span>Model:</span>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="general">General</SelectItem>
        <SelectItem value="ga">GA</SelectItem>
      </SelectContent>
    </Select>
  );
}
