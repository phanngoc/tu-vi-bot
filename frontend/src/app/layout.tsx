import type { ReactNode } from 'react';

import '../styles/globals.css';

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
