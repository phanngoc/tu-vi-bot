
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Not Found",
};

export default function NotFound() {
  return (
    <main className="text-black space-y-10 text-5xl font-bold flex flex-col items-center justify-center bg-main-white p-10 app-h-screen">
      <h1>
        404
      </h1>
      <h2>Not Found</h2>
    </main>
  );
}
