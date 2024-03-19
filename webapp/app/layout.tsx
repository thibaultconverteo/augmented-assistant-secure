import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { ModeToggle } from "@/components/ui/mode-toggle";
import ConverteoSvg from "@/components/svg/converteo-logo-svg";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Augmented Chatbot",
  description: "Poc of an augmented chatbot with AI for L'Oreal",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <div className="h-full flex w-screen">
            <div className="bg-gray-300 dark:bg-gray-950 flex justify-center p-5 h-full top-0 left-0 w-1/6">
              <ConverteoSvg className="dark:fill-white" />
            </div>
            <div className="flex-1 p-5">
              <div className="relative flex h-full max-w-full flex-1 flex-col overflow-hidden">
                <header className=" top-0 w-full">
                  <div className="flex h-14 max-w-screen-2xl items-center justify-center">
                    <div>
                      <h1 className="lg:text-2xl sm:text-xl font-semibold text-gray-700 dark:text-white">
                        Augmented Chatbot
                      </h1>
                    </div>

                    <div className="absolute lg:right-10 right-0 items-center">
                      <ModeToggle />
                    </div>
                  </div>
                </header>
                {children}
              </div>
            </div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
