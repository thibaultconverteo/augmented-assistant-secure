import { ReloadIcon } from "@radix-ui/react-icons";
import { twMerge } from "tailwind-merge";
import { useWindowSize } from "react-use";

import { Button } from "@/components/ui/button";

export function ButtonLoading() {
  const { width } = useWindowSize();

  return (
    <Button disabled>
      <ReloadIcon
        className={twMerge(width > 767 && "mr-2", "h-5 w-5 animate-spin")}
      />
      {width > 767 && "Send message"}
    </Button>
  );
}
