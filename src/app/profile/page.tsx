// app/profile/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import LoggedNav from "@/components/navbar/DashNavbar";
import { NeonGradientCard } from "@/components/ui/neon-gradient-card";
import { Button } from "@/components/ui/button";
import { MagicCard } from "@/components/ui/magic-card";
import FooterComponent from "@/components/footer/FooterComponent";

export default function ProfilePage() {
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();
  const [secretKey, setSecretKey] = useState<string>("");
  const [loadingKey, setLoadingKey] = useState(true);
  const [newsletterSubscribed, setNewsletterSubscribed] = useState(false);
  const [loadingNewsletter, setLoadingNewsletter] = useState(true);
  const [initializingKey, setInitializingKey] = useState(false);

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/login");
      return;
    }

    // Get blockchain secret key from session
    if (session?.user) {
      const bKey = (session.user as any).blockchainKey;
      if (bKey) {
        setSecretKey(bKey);
      }
      setLoadingKey(false);

      // Check newsletter subscription status
      checkNewsletterStatus();
    }
  }, [session, isPending, router]);

  const handleInitKey = async () => {
    setInitializingKey(true);
    try {
      const response = await fetch("/api/blockchain/init-user-key", {
        method: "POST",
      });
      const data = await response.json();
      if (response.ok) {
        setSecretKey(data.blockchainKey);
        // Refresh session to update the user object globally
        await authClient.getSession();
      } else {
        alert(data.error || "Failed to initialize key");
      }
    } catch (error) {
      alert("An error occurred");
    } finally {
      setInitializingKey(false);
    }
  };

  const checkNewsletterStatus = async () => {
    try {
      const response = await fetch("/api/newsletter/status");
      const data = await response.json();
      setNewsletterSubscribed(data.subscribed);
    } catch (error) {
      console.error("Failed to check newsletter status:", error);
    } finally {
      setLoadingNewsletter(false);
    }
  };

  const handleNewsletterUnsubscribe = async () => {
    if (!confirm("Are you sure you want to unsubscribe from the newsletter?")) {
      return;
    }

    try {
      const response = await fetch("/api/newsletter/unsubscribe", {
        method: "POST",
      });

      const data = await response.json();

      if (response.ok) {
        setNewsletterSubscribed(false);
        alert("Successfully unsubscribed from newsletter");
      } else {
        alert(data.error || "Failed to unsubscribe");
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
    }
  };

  const handleLogout = async () => {
    await authClient.signOut();
    router.push("/login");
  };

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDeleteAccount = async () => {
    if (!showDeleteConfirm) {
      setShowDeleteConfirm(true);
      return;
    }

    setIsDeleting(true);
    try {
      // Call the delete account API
      const response = await fetch("/api/auth/delete-account", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      console.log("API Response:", data);

      if (!response.ok) {
        const errorMsg = data.details || data.error || "Failed to delete account";
        throw new Error(errorMsg);
      }

      // Sign out and redirect to home page
      await authClient.signOut();
      router.push("/");
    } catch (error: any) {
      console.error("Error deleting account:", error);
      alert(`Failed to delete account: ${error.message || "Please try again."}`);
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  if (isPending || !session) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-foreground text-lg">Checking authentication...</p>
      </div>
    );
  }

  const user = session.user;

  return (
    <>
      <LoggedNav />

      <div className="min-h-screen bg-background pt-24 px-4 pb-12 flex flex-col items-center">
        {/* Header */}
        <div className="text-center mb-12 max-w-2xl">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Welcome, {user.name?.split(" ")[0] || "User"}!
          </h1>
          <p className="text-muted-foreground text-lg">
            Your personal dashboard for Nyaysetu AI.
          </p>
        </div>

        {/* Profile Card */}
        <div className={`w-full max-w-md relative ${newsletterSubscribed ? 'group' : ''}`}>
          {/* Golden glow effect for newsletter subscribers */}
          {newsletterSubscribed && (
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/20 via-amber-400/20 to-yellow-400/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-500 opacity-75 group-hover:opacity-100" />
          )}

          <MagicCard className={`w-full bg-card relative ${newsletterSubscribed ? 'border-2 border-yellow-400/30 shadow-2xl group-hover:shadow-yellow-500/30' : ''}`}>
            <div className="p-6 flex flex-col items-center">
              {/* Newsletter Premium Badge */}
              {newsletterSubscribed && (
                <div className="absolute top-4 right-4">
                  <span className="px-3 py-1 bg-gradient-to-r from-yellow-400 to-amber-500 text-yellow-900 text-xs font-bold rounded-full shadow-lg flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                    </svg>
                    PREMIUM
                  </span>
                </div>
              )}
              {/* User Name */}
              <h2 className="text-2xl font-bold text-foreground mb-6 text-center">
                {user.name || "User"}
              </h2>

              {/* Account info */}
              <div className="space-y-2 w-full text-left">
                <div className="flex">
                  <span className="text-muted-foreground font-medium w-28">Name:</span>
                  <span className="text-foreground">{user.name || "N/A"}</span>
                </div>

                <div className="flex">
                  <span className="text-muted-foreground font-medium w-28">Email:</span>
                  <span className="text-foreground">{user.email}</span>
                </div>

                <div className="flex flex-col">
                  <span className="text-muted-foreground font-medium mb-2">Secret Key:</span>
                  {loadingKey ? (
                    <span className="text-muted-foreground text-sm">Loading...</span>
                  ) : secretKey ? (
                    <div className="bg-muted p-3 rounded-md">
                      <span className="font-mono text-sm text-foreground break-all">{secretKey}</span>
                      <p className="text-xs text-yellow-500 mt-2">⚠️ Keep this key safe for blockchain access</p>
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2">
                      <span className="text-muted-foreground text-sm italic">Key not initialized</span>
                      <Button
                        onClick={handleInitKey}
                        disabled={initializingKey}
                        size="sm"
                        className="bg-yellow-600 hover:bg-yellow-700 text-white w-fit"
                      >
                        {initializingKey ? "Initializing..." : "Generate Blockchain Key"}
                      </Button>
                    </div>
                  )}
                </div>

                <div className="flex">
                  <span className="text-muted-foreground font-medium w-28">Email Status:</span>
                  <span className={user.emailVerified ? "text-green-500" : "text-yellow-500"}>
                    {user.emailVerified ? "Verified ✓" : "Pending"}
                  </span>
                </div>

                {/* Newsletter Status */}
                {!loadingNewsletter && newsletterSubscribed && (
                  <div className="flex items-center pt-2 border-t border-border/50 mt-2">
                    <span className="text-muted-foreground font-medium w-28">Newsletter:</span>
                    <span className="text-yellow-600 dark:text-yellow-400 font-medium flex items-center gap-1">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                      Subscribed
                    </span>
                  </div>
                )}
              </div>

              {/* Logout and Delete Account Buttons */}
              <div className="mt-8 w-full">
                {!showDeleteConfirm ? (
                  <div className="flex gap-3">
                    <Button
                      onClick={handleLogout}
                      variant="outline"
                      className="flex-1 border-red-500 text-red-500 hover:bg-red-50 dark:hover:bg-red-950"
                    >
                      Logout
                    </Button>
                    <Button
                      onClick={handleDeleteAccount}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                    >
                      Delete Account
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-sm text-red-500 text-center font-medium">
                      Are you sure? This action cannot be undone!
                    </p>
                    <div className="flex gap-2">
                      <Button
                        onClick={handleDeleteAccount}
                        disabled={isDeleting}
                        className="flex-1 bg-red-600 hover:bg-red-700 text-white"
                      >
                        {isDeleting ? "Deleting..." : "Yes, Delete"}
                      </Button>
                      <Button
                        onClick={() => setShowDeleteConfirm(false)}
                        disabled={isDeleting}
                        variant="outline"
                        className="flex-1"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </MagicCard>
        </div>

        {/* Premium Newsletter Subscription Card */}
        {!loadingNewsletter && newsletterSubscribed && (
          <div className="w-full max-w-md mt-6 relative group">
            {/* Golden glow effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/20 via-amber-400/20 to-yellow-400/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-500 opacity-75 group-hover:opacity-100" />

            {/* Main card */}
            <div className="relative bg-gradient-to-br from-yellow-50 via-amber-50 to-yellow-100 dark:from-yellow-900/30 dark:via-amber-900/40 dark:to-yellow-800/30 rounded-2xl p-6 border-2 border-yellow-400/50 dark:border-yellow-500/50 shadow-2xl group-hover:shadow-yellow-500/50 transition-all duration-500 group-hover:scale-[1.02]">
              {/* Shimmer overlay */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:translate-x-full transition-transform duration-1000 ease-in-out rounded-2xl" />

              {/* Content */}
              <div className="relative z-10">
                {/* Header with icon */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-yellow-400/30 dark:bg-yellow-500/20 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-yellow-700 dark:text-yellow-400">
                      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-yellow-900 dark:text-yellow-200">
                      Premium Subscriber
                    </h3>
                    <p className="text-xs text-yellow-700 dark:text-yellow-400">
                      NyaySetu Legal Newsletter
                    </p>
                  </div>
                  <div className="ml-auto">
                    <span className="px-3 py-1 bg-yellow-500/30 dark:bg-yellow-600/30 text-yellow-900 dark:text-yellow-200 text-xs font-bold rounded-full border border-yellow-600/50">
                      ACTIVE
                    </span>
                  </div>
                </div>

                {/* Subscription details */}
                <div className="space-y-2 bg-white/40 dark:bg-black/20 rounded-lg p-4 backdrop-blur-sm">
                  <div className="flex items-center gap-2 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-green-600 dark:text-green-400">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    <span className="text-yellow-900 dark:text-yellow-100 font-medium">
                      Weekly legal insights delivered
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-green-600 dark:text-green-400">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    <span className="text-yellow-900 dark:text-yellow-100 font-medium">
                      Exclusive legal updates
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-green-600 dark:text-green-400">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    <span className="text-yellow-900 dark:text-yellow-100 font-medium">
                      Email Status: <span className="text-green-600 dark:text-green-400">Verified ✓</span>
                    </span>
                  </div>
                </div>

                {/* CTA */}
                <div className="mt-4 flex items-center justify-between">
                  <p className="text-xs text-yellow-800 dark:text-yellow-300 italic">
                    Thank you for being a valued subscriber!
                  </p>
                  <button
                    onClick={handleNewsletterUnsubscribe}
                    className="text-xs text-yellow-700 dark:text-yellow-400 hover:text-red-600 dark:hover:text-red-400 underline underline-offset-2 transition-colors"
                  >
                    Unsubscribe
                  </button>
                </div>
              </div>

              {/* Corner decoration */}
              <div className="absolute top-3 right-3 text-yellow-600/20 dark:text-yellow-400/10">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
              </div>
            </div>
          </div>
        )}

        {/* Success Message */}
        <div className="mt-8 p-4 bg-green-500/10 border border-green-500/50 rounded-xl max-w-md w-full">
          <p className="text-green-500 text-center">
            You are successfully logged in!
          </p>
        </div>
      </div>
      <FooterComponent />
    </>
  );
}