"use client";
import { SparklesCore } from "../components/ui/sparkles";
import { useState, useEffect } from "react";

export function SparklesPreview() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const updateTheme = () => {
      setIsDark(document.documentElement.classList.contains("dark"));
    };

    updateTheme();

    const observer = new MutationObserver(updateTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });

    return () => observer.disconnect();
  }, []);
  return (
    <div className="h-screen w-full bg-background flex flex-col items-center justify-center overflow-hidden relative transition-colors duration-300">
      {/* Main title: keep same size as before */}
      <h1 className="md:text-7xl text-3xl lg:text-9xl font-bold text-center text-foreground relative z-20">
        NyaySetu
      </h1>

      {/* Sparkles container */}
      <div className="w-[40rem] h-40 relative mt-8">
        {/* Gradients */}
        <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-[2px] w-3/4 blur-sm" />
        <div className="absolute inset-x-20 top-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent h-px w-3/4" />
        <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-[5px] w-1/4 blur-sm" />
        <div className="absolute inset-x-60 top-0 bg-gradient-to-r from-transparent via-sky-500 to-transparent h-px w-1/4" />

        {/* Sparkles */}
        <SparklesCore
          background="transparent"
          minSize={0.4}
          maxSize={1}
          particleDensity={1200}
          className="w-full h-full"
          particleColor={isDark ? "#FFD700" : "#B45309"}
        />

        {/* Radial Gradient mask */}
        <div className="absolute inset-0 w-full h-full bg-background [mask-image:radial-gradient(350px_200px_at_top,transparent_20%,white)]"></div>
      </div>

      {/* Subtitle / features below sparkles */}
      <div className="text-center mt-12 space-y-4 max-w-3xl">
        <h2 className="text-xl md:text-2xl font-semibold text-foreground">
          AI-Powered Justice for Every Citizen
        </h2>

        <ul className="flex flex-col md:flex-row items-center justify-center gap-6 mt-4 text-muted-foreground text-sm md:text-base font-medium">
          <li className="before:content-['•'] before:text-foreground before:mr-2">Chatbot</li>
          <li className="before:content-['•'] before:text-foreground before:mr-2">IPC Section Prediction</li>
          <li className="before:content-['•'] before:text-foreground before:mr-2">Legal Draft Generator</li>
          <li className="before:content-['•'] before:text-foreground before:mr-2">Law & Judgement Updates</li>
        </ul>
      </div>
    </div>
  );
}
