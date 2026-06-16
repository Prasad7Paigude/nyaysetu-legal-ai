"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import NavbarComponent from "@/components/navbar/NavbarComponent";
import DashNavbar from "@/components/navbar/DashNavbar";
import FooterComponent from "@/components/footer/FooterComponent";
import { MagicCard } from "@/components/ui/magic-card";
import { useTheme } from "next-themes";
import { motion } from "framer-motion";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export default function NewsletterPage() {
    const [email, setEmail] = useState("");
    const [subscribed, setSubscribed] = useState(false);
    const [isSubscribed, setIsSubscribed] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const { resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
    const { data: session, isPending } = useSession();
    const router = useRouter();

    useEffect(() => {
        setMounted(true);
    }, []);

    // Check subscription status and pre-fill email when user logs in
    useEffect(() => {
        if (session?.user) {
            setEmail(session.user.email);
            checkSubscriptionStatus();
        }
    }, [session]);

    const checkSubscriptionStatus = async () => {
        try {
            const response = await fetch("/api/newsletter/status");
            const data = await response.json();
            setIsSubscribed(data.subscribed);
            if (data.subscribed) {
                setSubscribed(true);
            }
        } catch (error) {
            console.error("Failed to check subscription status:", error);
        }
    };

    const logoSrc = mounted && resolvedTheme === "dark" ? "/logo2.png" : "/logo.png";

    // Use explicit type for event
    const handleSubscribe = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");
        setSuccessMessage("");

        if (!session) {
            router.push("/login");
            return;
        }

        if (!email) return;
        setLoading(true);

        try {
            const response = await fetch("/api/newsletter/subscribe", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.error || "Failed to subscribe");
                if (data.userEmail) {
                    setEmail(data.userEmail);
                }
                return;
            }

            setSuccessMessage(data.message);
            setSubscribed(true);
            setIsSubscribed(true);
        } catch (error) {
            setError("An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleUnsubscribe = async () => {
        if (!session) return;
        setLoading(true);
        setError("");
        setSuccessMessage("");

        try {
            const response = await fetch("/api/newsletter/unsubscribe", { method: "POST" });
            const data = await response.json();

            if (!response.ok) {
                setError(data.error || "Failed to unsubscribe");
                return;
            }

            setSuccessMessage(data.message);
            setSubscribed(false);
            setIsSubscribed(false);
        } catch (error) {
            setError("An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
            {session ? <DashNavbar /> : <NavbarComponent />}

            {/* 1️⃣ Hero Section */}
            <section className="relative pt-32 pb-20 px-4 md:px-8 flex flex-col items-center text-center overflow-hidden">
                {/* Background Gradient */}
                <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary/10 via-background to-background opacity-50" />

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="max-w-4xl mx-auto"
                >
                    <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/70 mb-6 pb-2 leading-tight">
                        Legal Awareness, Delivered Simply.
                    </h1>
                    <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                        Weekly AI-curated insights on IPC sections, citizen rights, FIR procedures, and landmark Indian judgments.
                    </p>

                    {/* Error Message */}
                    {error && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 px-6 py-4 rounded-lg mb-4"
                        >
                            <p className="font-medium">{error}</p>
                        </motion.div>
                    )}

                    {/* Success Message */}
                    {successMessage && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-6 py-4 rounded-lg mb-4"
                        >
                            <p className="font-medium">{successMessage}</p>
                        </motion.div>
                    )}

                    {!subscribed ? (
                        <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
                            <input
                                type="email"
                                placeholder="Enter your email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={loading}
                                className="w-full px-4 py-3 rounded-lg border border-border bg-background focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                                required
                                suppressHydrationWarning
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="px-8 py-3 rounded-lg bg-primary text-primary-foreground font-bold hover:bg-primary/90 transition-colors shadow-lg active:scale-95 duration-200 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                            >
                                {loading ? "Subscribing..." : "Subscribe for Free"}
                            </button>
                        </form>
                    ) : (
                        <div className="space-y-4">
                            <motion.div
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-6 py-4 rounded-lg"
                            >
                                <p className="font-medium">You're subscribed. Welcome to NyaySetu Legal Brief.</p>
                            </motion.div>
                            {isSubscribed && (
                                <button
                                    onClick={handleUnsubscribe}
                                    disabled={loading}
                                    className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? "Unsubscribing..." : "Unsubscribe"}
                                </button>
                            )}
                        </div>
                    )}

                    <p className="mt-4 text-xs text-muted-foreground">
                        No spam. Educational use only. Unsubscribe anytime.
                    </p>
                </motion.div>
            </section>

            {/* 2️⃣ Value Proposition Section */}
            <section className="py-20 px-4 md:px-8 max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <FeatureCard
                        title="IPC Explained"
                        description="Break down complex IPC sections using real-world examples in plain language."
                        icon={<BookIcon />}
                    />
                    <FeatureCard
                        title="Judgment Updates"
                        description="Summaries of Supreme Court and High Court rulings that affect every citizen."
                        icon={<GavelIcon />}
                    />
                    <FeatureCard
                        title="Know Your Rights"
                        description="Practical guides on FIR filing, arrest rights, and police procedures."
                        icon={<ShieldIcon />}
                    />
                    <FeatureCard
                        title="AI Legal Briefs"
                        description="Content generated and reviewed using NyaySetu’s advanced AI engine."
                        icon={<BrainIcon />}
                    />
                </div>
            </section>

            {/* 3️⃣ Sample Newsletter Preview */}
            <section className="py-20 bg-muted/30 px-4 md:px-8">
                <div className="max-w-4xl mx-auto">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl font-bold mb-4">Why Subscribe to the NyaySetu Legal Newsletter</h2>
                        <p className="text-muted-foreground">Structured, reliable, and timely legal information</p>
                    </div>

                    <motion.div
                        initial={{ y: 40, opacity: 0 }}
                        whileInView={{ y: 0, opacity: 1 }}
                        viewport={{ once: true }}
                        className="bg-card border border-border rounded-xl shadow-2xl overflow-hidden"
                    >
                        <div className="bg-primary/5 p-4 border-b border-border flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-400" />
                            <div className="w-3 h-3 rounded-full bg-yellow-400" />
                            <div className="w-3 h-3 rounded-full bg-green-400" />
                            <div className="ml-4 text-xs text-muted-foreground font-mono">NyaySetu Legal Newsletter</div>
                        </div>
                        <div className="p-8 md:p-12 space-y-6 leading-relaxed">
                            <p className="text-foreground">
                                The NyaySetu Legal Newsletter provides structured, reliable, and timely legal information to support informed decision-making. Subscribers receive periodic updates on significant legislative changes, judicial developments, and regulatory guidance relevant to their jurisdiction.
                            </p>

                            <div>
                                <h3 className="text-xl font-bold text-foreground mb-4">Key Inclusions:</h3>

                                <div className="space-y-4 text-muted-foreground">
                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">📋 Legal Highlights:</h4>
                                        <p>Concise summaries of important rulings, amendments, and policy changes issued during the period.</p>
                                    </div>

                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">🔍 Detailed Analysis:</h4>
                                        <p>Clear explanations of notable legal updates, along with their implications for individuals, professionals, and organizations.</p>
                                    </div>

                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">✅ Compliance Guidance:</h4>
                                        <p>Practical insights on regulatory requirements and procedural changes that may affect stakeholders.</p>
                                    </div>

                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">🔮 Future Legal Developments:</h4>
                                        <p>Advance information on proposed bills, pending judgments, and regulatory initiatives expected to shape the legal landscape.</p>
                                    </div>

                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">🎯 Credibility and Neutrality:</h4>
                                        <p>All content is researched, verified, and presented objectively, without advocacy or bias.</p>
                                    </div>

                                    <div>
                                        <h4 className="font-semibold text-foreground mb-2">🔓 Unsubscribe Flexibility:</h4>
                                        <p>Subscribers may opt out at any time through a simple unsubscribe option.</p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
                                <p className="text-sm text-yellow-800 dark:text-yellow-200">
                                    <span className="font-bold">Disclaimer:</span> This newsletter is intended for informational purposes only and does not constitute legal advice. Readers should seek professional counsel before relying on any information provided.
                                </p>
                            </div>

                            <div className="text-center pt-4">
                                <p className="text-sm text-muted-foreground italic">
                                    <span className="font-semibold text-primary">About NyaySetu:</span> NyaySetu is committed to enhancing legal awareness by delivering structured, accessible, and accurate legal information to the public.
                                </p>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* 4️⃣ Target Audience */}
            <section className="py-20 px-4 md:px-8 max-w-5xl mx-auto">
                <div className="grid md:grid-cols-2 gap-12 items-center">
                    <div>
                        <h2 className="text-3xl font-bold mb-6">Who Is This For?</h2>
                        <ul className="space-y-4">
                            {[
                                "Citizens interested in understanding their rights",
                                "Law students and judicial service aspirants",
                                "Social workers and NGO volunteers",
                                "Startups and small business owners",
                                "First-time FIR filers and victims seeking guidance"
                            ].map((item, i) => (
                                <motion.li
                                    key={i}
                                    initial={{ opacity: 0, x: -20 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                    viewport={{ once: true }}
                                    className="flex items-center gap-3 text-lg"
                                >
                                    <span className="text-green-500">✓</span> {item}
                                </motion.li>
                            ))}
                        </ul>
                    </div>
                    <div className="relative h-64 md:h-full min-h-[300px] rounded-2xl bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center p-8">
                        <div className="text-center flex flex-col items-center">
                            <img src={logoSrc} alt="NyaySetu Logo" width={120} height={120} className="mb-4 object-contain" />
                            <p className="font-bold text-xl">Democratizing Legal Knowledge</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* 5️⃣ Social Impact */}
            <section className="py-20 bg-background px-4 md:px-8 text-center bg-dot-black/[0.2] dark:bg-dot-white/[0.2]">
                <div className="max-w-3xl mx-auto">
                    <h2 className="text-3xl font-bold mb-6">Why NyaySetu’s Newsletter Matters</h2>
                    <p className="text-lg text-muted-foreground mb-8">
                        Access to legal knowledge is expensive and complex. In a country of 1.4 billion, awareness is the first step towards justice. We are bridging the gap between complex law and the common citizen.
                    </p>
                    <div className="flex flex-wrap justify-center gap-4">
                        <span className="px-4 py-2 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 text-sm font-medium">Empathetic</span>
                        <span className="px-4 py-2 rounded-full bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300 text-sm font-medium">Mission-Driven</span>
                        <span className="px-4 py-2 rounded-full bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300 text-sm font-medium">Non-Commercial</span>
                    </div>
                </div>
            </section>

            {/* 6️⃣ Final CTA */}
            <section className="py-24 px-4 md:px-8 text-center bg-gradient-to-t from-primary/5 to-transparent">
                <h2 className="text-3xl font-bold mb-8">Thousands already trust NyaySetu for legal awareness.</h2>
                {!subscribed ? (
                    <div className="flex flex-col items-center">
                        <Link href="#hero" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
                            <button className="px-8 py-3 text-lg bg-primary text-white rounded-lg font-bold hover:bg-primary/90 transition-colors shadow-lg active:scale-95 duration-200">
                                Subscribe Now (it’s free)
                            </button>
                        </Link>
                    </div>
                ) : (
                    <p className="text-green-600 font-medium text-lg">You are part of the movement!</p>
                )}
            </section>

            <FooterComponent />

            {/* Footer Disclaimer Override/Addition */}
            <div className="bg-background py-4 text-center border-t border-border">
                <p className="text-xs text-muted-foreground">
                    For educational purposes only. Not a substitute for professional legal advice.
                </p>
            </div>
        </div>
    );
}

function FeatureCard({ title, description, icon }: { title: string, description: string, icon: React.ReactNode }) {
    return (
        <MagicCard
            className="w-full h-full p-6 flex flex-col items-start gap-4 hover:scale-105 transition-transform duration-300 shadow-sm hover:shadow-md cursor-pointer rounded-lg"
            gradientColor={"#D9D9D955"}
        >
            <div className="p-3 rounded-lg bg-primary/10 text-primary dark:text-white dark:bg-primary/20">
                {icon}
            </div>
            <h3 className="text-xl font-bold">{title}</h3>
            <p className="text-sm text-muted-foreground">{description}</p>
        </MagicCard>
    );
}

// Simple Icons
const BookIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" /><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" /></svg>
);
const GavelIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m14 13-7.5 7.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L11 10l-4-4 6-6 4 4 6 6-4 4-6-6Z" /><path d="m16 16 3-3" /></svg>
);
const ShieldIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>
);
const BrainIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" /><path d="M12 1v5" /><path d="M12 18v5" /><path d="m4.9 4.9 3.6 3.6" /><path d="m15.5 15.5 3.6 3.6" /><path d="M1 12h5" /><path d="M18 12h5" /><path d="m4.9 19.1 3.6-3.6" /><path d="m15.5 8.5 3.6-3.6" /></svg>
);
