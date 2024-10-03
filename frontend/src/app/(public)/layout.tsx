import type { ReactNode } from 'react';

export default function Layout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <main className="w-full app-min-h-screen flex justify-center items-center bg-tarot-color">
      <div className="overflow-hidden absolute">
        <div className="bg-tarot opacity-15 animate-infinity-bg bg-repeat-x w-[5076px] h-svh"></div>
        <div className="absolute left-0 top-0 w-full h-full flex justify-center items-center pointer-events-none after:content-[''] after:block after:absolute after:w-1/4 after:py-[12%] after:rounded-full after:bg-luminescent-light">
          <div className="w-full relative">
            <div className="rotate-0 animate-[rotateIt_21s_linear_infinite] before:content-[''] before:block before:w-full before:pb-[100%] before:bg-luminescent-one before:bg-no-repeat before:bg-scroll before:bg-black/0 before:bg-cover before:bg-center before:animate-[rotateOp_1.8s_ease-in-out_infinite]"></div>
            <div className="absolute left-0 top-0 w-full h-full rotate-0 animate-[rotateIt_33s_linear_infinite_reverse] before:content-[''] before:block before:w-full before:pb-[100%] before:bg-luminescent-two before:bg-no-repeat before:bg-scroll before:bg-black/0 before:bg-cover before:bg-center before:animate-[rotateOp_1.5s_ease-in-out_infinite]"></div>
          </div>
        </div>
      </div>
      {children}
    </main>
  );
}
