import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import Script from "next/script"; // <-- Ajout

import Navbar from "./components/Navbar";
import Image from "next/image";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Good Karma - Reddit Post Optimizer",
    template: "%s | Good Karma",
  },
  description:
    "Good Karma helps you optimize your Reddit posts for better engagement. Analyze your drafts, get actionable advice, and discover the best keywords and similar posts.",
  keywords: [
    "Reddit",
    "SEO",
    "Post Optimizer",
    "Post Analyzer",
    "Reddit SEO",
    "Post Performance",
    "Keyword Suggestions",
    "Engagement",
    "Advice",
    "KPI",
    "Good Karma",
    "Social Media",
    "Content Analysis",
  ],
  authors: [{ name: "Morlana Team", url: "https://good-karma.io" }],
  creator: "Morlana Team",
  openGraph: {
    title: "Good Karma - Reddit Post Analyzer",
    description:
      "Optimize your Reddit posts with actionable advice, KPIs, and keyword suggestions.",
    url: "https://good-karma.io",
    siteName: "Good Karma",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Good Karma - Reddit Post Analyzer",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Good Karma - Reddit Post Analyzer",
    description:
      "Optimize your Reddit posts with actionable advice, KPIs, and keyword suggestions.",
    site: "@goodkarma_app",
    creator: "@goodkarma_app",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-snippet": -1,
      "max-image-preview": "large",
      "max-video-preview": -1,
    },
  },
  themeColor: "#ff5700",
  manifest: "/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Navbar />
        <main className="md:ml-56">{children}</main>
      </body>
    </html>
  );
}
