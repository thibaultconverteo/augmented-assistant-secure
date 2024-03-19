import { Button } from "@/components/ui/button";
import { TrashIcon } from "@radix-ui/react-icons";
import React, { useState, useEffect } from "react";

export default function ButtonDelete() {
  const [notChatHistory, setNotChatHistory] = useState(Boolean);

  const clearLocalStorage = () => {
    localStorage.removeItem("chat_history");
    setNotChatHistory(true);
  };

  useEffect(() => {
    // Check if 'chat_history' exists in local storage
    const checkChatHistory = () => {
      // Check if 'chat_history' exists in local storage
      const hasChatHistory = localStorage.getItem("chat_history") !== null;
      setNotChatHistory(!hasChatHistory);
    };
    // Check on mount
    checkChatHistory();

    // Check when localStorage changes
    window.addEventListener("storage", checkChatHistory);

    // Clean up event listener
    return () => window.removeEventListener("storage", checkChatHistory);
  }, []);
  return (
    <Button
      variant="destructive"
      onClick={clearLocalStorage}
      size="icon"
      disabled={notChatHistory}
    >
      <TrashIcon className="h-5 w-5" />
    </Button>
  );
}
