import { ReloadIcon } from "@radix-ui/react-icons";

import { Button } from "@/components/ui/button";

export function ButtonLoading() {
  return (
    <Button disabled>
      <ReloadIcon className="h-4 w-4 animate-spin" />
    </Button>
  );
}
