"use client";
import { SparklesPreview } from "../components/sparclesUi";
import NavbarComponent from "@/components/navbar/NavbarComponent";
import { MacbookScroll } from "@/components/ui/macbook-scroll";
import FooterComponent from "@/components/footer/FooterComponent";
import { MagicCard } from "@/components/ui/magic-card";
import { ShinyButton } from "@/components/ui/shiny-button";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <NavbarComponent />
      <SparklesPreview />

      <div className="bg-background pt-24 px-4 pb-12 transition-colors duration-300">
        <div className="max-w-7xl mx-auto">
          {/* Heading and subheading */}
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">
              Powerful AI Features
            </h2>
            <p className="mt-2 text-muted-foreground text-sm md:text-base">
              Experience the next generation of legal technology with our advanced
              AI agents and intelligent automation.
            </p>
          </div>

          {/* Cards grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-[1400px] mx-auto">
            {/* Card 1 – Chatbot */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22c4.97 0 9-3.58 9-8s-4.03-8-9-8-9 3.58-9 8c0 2.64 1.32 5 3.43 6.57L5 22l4.21-1.31C10.1 21.56 11.03 22 12 22z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Chatbot</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Explain IPC sections and legal concepts in simple English, analyze incidents, and guide users on applicable laws and next steps.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Launch Chatbot
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 2 – IPC Section Prediction */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M12 7v5l3 3"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">IPC Section Prediction</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Automatically predict the most relevant IPC Section(s) based on a user’s incident description provided in multiple formats. Ensures citizens understand which laws apply.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Start Prediction
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 3 – Legal Draft Generator */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 2l7 4v6c0 5-3.5 9-7 10-3.5-1-7-5-7-10V6l7-4z"></path>
                    <path d="M9 12h6"></path>
                    <path d="M9 16h4"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Legal Draft Generator</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Automate the creation of legal documents using predefined templates and dynamic questioning.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Generate Draft
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 4 – Judgement Updates */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 6h-8l-2-3H3v17h18V6z"></path>
                    <path d="M3 13h18"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Judgement Updates</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Automatically fetch legal news, updates, and judgments; deliver via website or automated newsletter.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    View Updates
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>
          </div>
        </div>
      </div>

      {/* <MacbookScroll src="/macbook-image.png" /> */}

      <div className="bg-background pt-24 px-4 pb-12 transition-colors duration-300">
        <div className="max-w-7xl mx-auto">
          {/* Heading and subheading */}
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">
              Key Advantages
            </h2>
            <p className="mt-2 text-muted-foreground text-sm md:text-base">
              Discover the powerful advantages that make NyaySetu the leading choice for
              legal technology solutions.
            </p>
          </div>

          {/* Cards grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-[1400px] mx-auto">
            {/* Card 1 – Smart Automated Document */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22c4.97 0 9-3.58 9-8s-4.03-8-9-8-9 3.58-9 8c0 2.64 1.32 5 3.43 6.57L5 22l4.21-1.31C10.1 21.56 11.03 22 12 22z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Smart Automated Document</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Intelligent document processing with AI-powered analysis, formatting, and legal compliance checking.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Start Processing
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 2 – Multi Agent Collaboration */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M12 7v5l3 3"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Multi Agent Collaboration</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Coordinated AI agents working together to provide comprehensive legal solutions and insights.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Collaborate
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 3 – Agentic Approach */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 2l7 4v6c0 5-3.5 9-7 10-3.5-1-7-5-7-10V6l7-4z"></path>
                    <path d="M9 12h6"></path>
                    <path d="M9 16h4"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">Agentic Approach</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Advanced AI agents that autonomously handle complex legal tasks with intelligent decision-making capabilities.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Explore Agents
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Card 4 – 24/7 Availability */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" className="stroke-foreground" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 6h-8l-2-3H3v17h18V6z"></path>
                    <path d="M3 13h18"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2 min-h-[56px]">24/7 Availability</h3>
                <p className="text-sm text-muted-foreground flex-grow min-h-[80px]">
                  Round-the-clock legal assistance and document processing without any downtime.
                </p>
                <Link href="/login" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Get Help Now
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>
          </div>
        </div>
      </div>

      {/* Macbook Scroll Effect */}
      <FooterComponent />
    </>
  );
}
