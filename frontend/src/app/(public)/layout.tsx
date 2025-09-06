import type { ReactNode } from 'react';

export default function Layout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <main className="w-full app-min-h-screen flex justify-center items-center bg-gradient-to-br from-mystic-dark via-tarot-color to-mystic-purple relative overflow-hidden">
      {/* Enhanced Mystical Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Animated pattern background */}
        <div className="bg-tarot opacity-10 bg-repeat-x w-[5076px] h-svh"></div>
        
        {/* Floating mystical particles */}
        <div className="absolute inset-0">
          {Array.from({ length: 20 }).map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-mystic-gold/30 rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`
              }}
            />
          ))}
        </div>
        
        {/* Central luminescent orbs */}
        <div className="absolute left-0 top-0 w-full h-full flex justify-center items-center pointer-events-none">
          {/* Main central light */}
          <div className="w-1/3 h-1/3 bg-luminescent-light rounded-full opacity-20"></div>
          
          {/* Rotating mystical elements */}
          <div className="absolute w-full h-full">
            <div className="rotate-0 before:content-[''] before:block before:w-full before:pb-[100%] before:bg-luminescent-one before:bg-no-repeat before:bg-scroll before:bg-black/0 before:bg-cover before:bg-center opacity-20"></div>
            <div className="absolute left-0 top-0 w-full h-full rotate-0 before:content-[''] before:block before:w-full before:pb-[100%] before:bg-luminescent-two before:bg-no-repeat before:bg-scroll before:bg-black/0 before:bg-cover before:bg-center opacity-15"></div>
          </div>
        </div>
        
        {/* Mystical border effects */}
        <div className="absolute inset-0 border border-mystic-gold/5 rounded-3xl m-4"></div>
        <div className="absolute inset-0 border border-mystic-amber/10 rounded-2xl m-8"></div>
      </div>
      
      {/* Content */}
      <div className="relative z-10 w-full flex justify-center items-center p-4">
        {children}
      </div>
    </main>
  );
}
