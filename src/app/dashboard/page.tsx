// app/dashboard/page.tsx
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// Components
import LoggedNav from "@/components/navbar/DashNavbar";
import { SparklesPreview } from "@/components/sparclesUi";
import { MacbookScroll } from "@/components/ui/macbook-scroll";
import { MagicCard } from "@/components/ui/magic-card";
import { ShinyButton } from "@/components/ui/shiny-button";
import FooterComponent from "@/components/footer/FooterComponent";
import Link from "next/link";

// Auth
import { authClient } from "@/lib/auth-client";

export default function DashboardPage() {
  const router = useRouter();

  // Get session from Better Auth
  const { data: session, isPending } = authClient.useSession();

  // Logout
  const handleLogout = async () => {
    try {
      await authClient.signOut();
      router.push("/login");
    } catch (err) {
      console.error("Logout error:", err);
    }
  };

  // Redirect user if not logged in
  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login");
    }
  }, [isPending, session, router]);

  // Automatically Initialize Blockchain Key (For OAuth users)
  useEffect(() => {
    const initKey = async () => {
      // @ts-ignore - blockchainKey is a custom field
      if (session?.user && !session.user.blockchainKey) {
        try {
          await fetch("/api/blockchain/init-user-key", { method: "POST" });
          console.log("Blockchain key initialized for OAuth user.");
        } catch (error) {
          console.error("Failed to init key:", error);
        }
      }
    };
    initKey();
  }, [session]);

  // Loading screen
  if (isPending) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-white">Loading...</p>
        </div>
      </div>
    );
  }

  // Safety fallback
  if (!session) return null;

  const user = session.user;

  return (
    <>
      <LoggedNav />
      <SparklesPreview />

      <div className="min-h-screen bg-background pt-24 px-4 pb-12 transition-colors duration-300">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Section */}
          <div className="mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
              Welcome back, {user.name || "User"}!
            </h1>
            <p className="text-muted-foreground text-lg">
              Access your legal AI tools and manage your account
            </p>
          </div>

          {/* Section Title */}
          <div className="text-center max-w-2xl mx-auto mb-8">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">Your AI Legal Tools</h2>
            <p className="mt-2 text-muted-foreground text-sm md:text-base">
              Choose from our powerful AI features to get started
            </p>
          </div>

          {/* TOOLS GRID */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-[1400px] mx-auto">

            {/* Chatbot */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" fill="none" className="stroke-foreground" strokeWidth="1.7">
                    <path d="M12 22c4.97 0 9-3.58 9-8s-4.03-8-9-8-9 3.58-9 8c0 2.64 1.32 5 3.43 6.57L5 22l4.21-1.31C10.1 21.56 11.03 22 12 22z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">Chatbot</h3>
                <p className="text-sm text-muted-foreground flex-grow">
                  Get instant legal guidance for IPC sections.
                </p>
                <Link href="/chatbot" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Launch Chatbot
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* IPC Prediction */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" fill="none" className="stroke-foreground" strokeWidth="1.7">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M12 7v5l3 3"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">IPC Section Prediction</h3>
                <p className="text-sm text-muted-foreground flex-grow">
                  Predict relevant IPC sections from incident details.
                </p>
                <Link href="/ipcpredication" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Start Prediction
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Draft Generator */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" fill="none" className="stroke-foreground" strokeWidth="1.7">
                    <path d="M12 2l7 4v6c0 5-3.5 9-7 10-3.5-1-7-5-7-10V6l7-4z"></path>
                    <path d="M9 12h6"></path>
                    <path d="M9 16h4"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">Legal Draft Generator</h3>
                <p className="text-sm text-muted-foreground flex-grow">
                  Generate court-ready legal drafts instantly.
                </p>
                <Link href="/generatedraft" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    Generate Draft
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

            {/* Judgment Updates */}
            <MagicCard className="w-full h-auto hover:scale-105 transition-transform rounded-lg">
              <div className="p-6 text-foreground flex flex-col h-full">
                <div className="mb-4">
                  <svg width="38" height="38" fill="none" className="stroke-foreground" strokeWidth="1.7">
                    <path d="M21 6h-8l-2-3H3v17h18V6z"></path>
                    <path d="M3 13h18"></path>
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">Judgement Updates</h3>
                <p className="text-sm text-muted-foreground flex-grow">
                  Latest judgements, legal updates, amendments.
                </p>
                <Link href="/newsletter" className="w-full">
                  <ShinyButton className="mt-4 bg-primary text-primary-foreground dark:bg-accent dark:text-accent-foreground">
                    View Updates
                  </ShinyButton>
                </Link>
              </div>
            </MagicCard>

          </div>

          {/* Recent Activity */}
          <div className="mt-12 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-foreground mb-6">Recent Activity</h2>
            <MagicCard className="w-full rounded-lg">
              <div className="p-6">
                <h3 className="text-2xl font-bold text-foreground text-center mb-6">More features coming soon</h3>
                <p className="text-muted-foreground text-center py-8">
                  No recent activity yet.
                </p>
              </div>
            </MagicCard>
          </div>
        </div>

        {/* <MacbookScroll src="/macbook-image.png" /> */}
      </div>
      <FooterComponent />
    </>
  );
}