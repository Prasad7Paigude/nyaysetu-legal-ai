"use client";

import React, { useState, useEffect } from "react";
import { IconScale, IconMicrophone } from "@tabler/icons-react";
import { Button } from "@/components/ui/button";
import NavbarComponent from "@/components/navbar/NavbarComponent";
import DashNavbar from "@/components/navbar/DashNavbar";
import FooterComponent from "@/components/footer/FooterComponent";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function IPCPredictionPage() {
    const [incidentDescription, setIncidentDescription] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const { data: session, isPending } = useSession();
    const router = useRouter();

    const handlePredict = async () => {
        if (!incidentDescription.trim()) return;

        setIsLoading(true);
        setResult(null);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_IPC_API_URL || 'https://ipc-section.onrender.com';
            const response = await fetch(`${apiUrl}/ipc/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                },
                body: JSON.stringify({
                    text: incidentDescription
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get prediction');
            }

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error("Error fetching prediction:", error);
            // Optional: Set an error state to show to user
        } finally {
            setIsLoading(false);
        }
    };

    // Show loading state while checking auth
    if (isPending) {
        return (
            <div className="min-h-screen w-full bg-background flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Loading...</p>
                </div>
            </div>
        );
    }

    // If not authenticated, show login prompt
    if (!session) {
        return (
            <div className="min-h-screen w-full bg-background flex flex-col">
                <NavbarComponent />

                <div className="flex-1 flex flex-col items-center justify-center p-4 pt-32 pb-20">
                    <div className="w-full max-w-3xl flex flex-col items-center text-center space-y-6">

                        <div className="bg-muted p-4 rounded-2xl shadow-sm">
                            <IconScale className="w-8 h-8 text-primary" stroke={2} />
                        </div>

                        <h1 className="text-4xl md:text-5xl font-bold text-foreground">
                            IPC Section Prediction
                        </h1>

                        <p className="text-muted-foreground text-lg max-w-2xl leading-relaxed">
                            Describe the incident in detail and our AI will predict the most relevant IPC sections with confidence scores and legal guidance.
                        </p>

                        {/* Login Required Card */}
                        <div className="w-full bg-card rounded-2xl shadow-2xl overflow-hidden border border-border mt-8">
                            <div className="bg-primary/5 dark:bg-primary/10 p-4 border-b border-border flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-red-400" />
                                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                                <div className="w-3 h-3 rounded-full bg-green-400" />
                                <div className="ml-4 text-xs text-muted-foreground font-mono">Authentication Required</div>
                            </div>

                            <div className="p-8 md:p-12 text-center space-y-6">
                                <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
                                    <p className="text-lg font-semibold text-yellow-800 dark:text-yellow-200 mb-2">
                                        🔒 Login Required
                                    </p>
                                    <p className="text-yellow-700 dark:text-yellow-300">
                                        Please log in or sign up to use the IPC Section Prediction feature.
                                    </p>
                                </div>

                                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                    <Link href="/login">
                                        <Button className="px-8 py-6 text-lg font-semibold bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg rounded-xl">
                                            Log In
                                        </Button>
                                    </Link>
                                    <Link href="/signup">
                                        <Button className="px-8 py-6 text-lg font-semibold bg-secondary hover:bg-secondary/90 text-secondary-foreground shadow-lg rounded-xl">
                                            Sign Up
                                        </Button>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <FooterComponent />
            </div>
        );
    }

    // Authenticated user - show full functionality
    return (
        <div className="min-h-screen w-full bg-background flex flex-col">
            <DashNavbar />

            <div className="flex-1 flex flex-col items-center justify-center p-4 pt-32 pb-20">
                <div className="w-full max-w-3xl flex flex-col items-center text-center space-y-6">

                    <div className="bg-muted p-4 rounded-2xl shadow-sm">
                        <IconScale className="w-8 h-8 text-primary" stroke={2} />
                    </div>

                    <h1 className="text-4xl md:text-5xl font-bold text-foreground">
                        IPC Section Prediction
                    </h1>

                    <p className="text-muted-foreground text-lg max-w-2xl leading-relaxed">
                        Describe the incident in detail and our AI will predict the most relevant IPC sections with confidence scores and legal guidance.
                    </p>

                    <div className="w-full bg-card rounded-2xl shadow-2xl overflow-hidden border border-border">
                        <div className="bg-primary/5 dark:bg-primary/10 p-4 border-b border-border flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-400" />
                            <div className="w-3 h-3 rounded-full bg-yellow-400" />
                            <div className="w-3 h-3 rounded-full bg-green-400" />
                            <div className="ml-4 text-xs text-muted-foreground font-mono">IPC Prediction Tool</div>
                        </div>

                        <div className="p-6 md:p-8 text-left space-y-4">
                            <h2 className="text-xl font-semibold text-primary/80">Describe the Incident</h2>
                            <p className="text-muted-foreground text-sm">
                                Provide as much detail as possible about what happened, including date, time, location, and parties involved.
                            </p>

                            <div className="relative">
                                <textarea
                                    className="w-full min-h-[80px] p-4 pr-12 rounded-xl border-2 border-primary/20 bg-background text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary transition-all resize-none text-base"
                                    placeholder="E.g., 'Yesterday evening around 7 PM, someone broke into my parked car near the market and stole my laptop bag containing important documents and cash worth ₹50,000...'"
                                    value={incidentDescription}
                                    onChange={(e) => setIncidentDescription(e.target.value)}
                                />

                                <button
                                    disabled
                                    className="absolute bottom-4 right-4 p-2 rounded-full bg-muted/50 text-muted-foreground/40 cursor-not-allowed"
                                    title="Voice input coming soon"
                                >
                                    <IconMicrophone className="w-5 h-5" stroke={2} />
                                </button>
                            </div>

                            <Button
                                onClick={handlePredict}
                                disabled={isLoading || !incidentDescription.trim()}
                                className="w-full py-6 text-lg font-semibold bg-primary hover:bg-primary/90 text-primary-foreground dark:bg-[#CFAF6B] dark:text-[#0C1A24] dark:hover:bg-[#CFAF6B]/90 shadow-lg rounded-xl transition-all"
                            >
                                {isLoading ? (
                                    <div className="flex items-center gap-2">
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin dark:border-black/30 dark:border-t-black" />
                                        Analyzing...
                                    </div>
                                ) : "Predict IPC Section"}
                            </Button>

                            {result && (
                                <div className="mt-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                    <div className="flex items-center gap-4 mb-6">
                                        <div className="h-px bg-border flex-1" />
                                        <span className="text-sm font-medium text-muted-foreground uppercase tracking-widest">Analysis Result</span>
                                        <div className="h-px bg-border flex-1" />
                                    </div>

                                    {/* Analyzed Input Section */}
                                    <div className="bg-muted/30 rounded-xl p-5 border border-border/50">
                                        <p className="text-xs font-semibold text-muted-foreground uppercase mb-2 tracking-wide">
                                            Analyzed Incident
                                        </p>
                                        <p className="text-foreground/90 italic border-l-2 border-primary/30 pl-3 leading-relaxed">
                                            "{result.input_text}"
                                        </p>
                                    </div>

                                    {/* Main Prediction Card */}
                                    <div className="bg-card rounded-xl border border-primary/20 shadow-sm overflow-hidden">
                                        <div className="bg-primary/5 p-6 border-b border-primary/10">
                                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                                                <div>
                                                    <div className="flex items-center gap-3 mb-1">
                                                        <h3 className="text-3xl font-bold text-primary dark:text-[#CFAF6B]">
                                                            {result.prediction.ipc_section}
                                                        </h3>
                                                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${parseInt(result.prediction.confidence) > 70 ? 'bg-green-500/10 text-green-600 border-green-500/20' : parseInt(result.prediction.confidence) > 40 ? 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20' : 'bg-red-500/10 text-red-600 border-red-500/20'}`}>
                                                            {result.prediction.confidence} Match
                                                        </span>
                                                    </div>
                                                    <p className="text-lg font-medium text-foreground">
                                                        {result.prediction.title}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="p-6 space-y-6">
                                            {/* Explanation */}
                                            <div>
                                                <h4 className="flex items-center gap-2 font-semibold text-foreground mb-2">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" /></svg>
                                                    Why this applies?
                                                </h4>
                                                <p className="text-muted-foreground dark:text-gray-300 leading-relaxed pl-7">
                                                    {result.explanation}
                                                </p>
                                            </div>

                                            {/* Suggestion */}
                                            <div className="bg-blue-50 dark:bg-blue-900/10 rounded-lg p-4 border border-blue-100 dark:border-blue-900/30">
                                                <h4 className="flex items-center gap-2 font-semibold text-blue-700 dark:text-blue-300 mb-2">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" /></svg>
                                                    Recommended Action
                                                </h4>
                                                <p className="text-blue-600/90 dark:text-blue-200 leading-relaxed">
                                                    {result.suggestion}
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex justify-center mt-4">
                                        <p className="text-center text-xs text-red-600 dark:text-red-400 font-medium max-w-xl bg-red-50 dark:bg-red-900/10 px-6 py-3 rounded-full border border-red-100 dark:border-red-900/30 shadow-sm">
                                            <span className="font-bold uppercase tracking-wider mr-2 text-red-700 dark:text-red-300">Disclaimer:</span>
                                            {result.disclaimer}
                                        </p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            <FooterComponent />
        </div>
    );
}
