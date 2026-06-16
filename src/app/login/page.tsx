// app/login/page.tsx
"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { IconBrandGithub, IconBrandGoogle, IconMail, IconChevronDown, IconChevronUp } from "@tabler/icons-react";
import { authClient } from "@/lib/auth-client";
import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler";

function LoginForm() {
  const searchParams = useSearchParams();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [socialLoading, setSocialLoading] = useState<string | null>(null);
  const [showEmailForm, setShowEmailForm] = useState(false);

  // Check if already logged in on page load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data } = await authClient.getSession();
        if (data?.user) {
          window.location.href = "/dashboard";
          return;
        }
      } catch (e) {
        // Not logged in
      }
      setInitialLoading(false);
    };
    checkAuth();
  }, []);

  useEffect(() => {
    if (searchParams.get("verified") === "true") {
      setSuccess("Email verified successfully! You can now log in.");
      setShowEmailForm(true); // Auto-expand email form when coming from verification
    }
    // Handle OAuth errors
    const errorParam = searchParams.get("error");
    if (errorParam) {
      setError(decodeURIComponent(errorParam));
    }
  }, [searchParams]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  // ============================================
  // GITHUB LOGIN
  // ============================================
  const handleGitHubLogin = async () => {
    setError("");
    setSocialLoading("github");

    try {
      await authClient.signIn.social({
        provider: "github",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("GitHub login error:", err);
      setError(err instanceof Error ? err.message : "GitHub login failed");
      setSocialLoading(null);
    }
  };

  // ============================================
  // GOOGLE LOGIN
  // ============================================
  const handleGoogleLogin = async () => {
    setError("");
    setSocialLoading("google");

    try {
      await authClient.signIn.social({
        provider: "google",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("Google login error:", err);
      setError(err instanceof Error ? err.message : "Google login failed");
      setSocialLoading(null);
    }
  };

  // ============================================
  // EMAIL/PASSWORD LOGIN
  // ============================================
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const { data, error: signInError } = await authClient.signIn.email({
        email: formData.email,
        password: formData.password,
      });

      if (signInError) {
        if (signInError.status === 403) {
          setError("Please verify your email before logging in.");
          setLoading(false);
          return;
        }
        throw new Error(signInError.message || "Login failed");
      }

      if (data?.user) {
        setSuccess("Login successful! Redirecting...");
        window.location.href = "/dashboard";
      } else {
        throw new Error("Login failed - no user data");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid credentials");
      setLoading(false);
    }
  };

  if (initialLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-black">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center p-8 bg-gray-50 dark:bg-black min-h-screen relative transition-colors duration-300">
      <div className="absolute top-4 right-4">
        <AnimatedThemeToggler />
      </div>
      <div className="shadow-input mx-auto w-full max-w-md rounded-2xl p-6 md:p-8 bg-white dark:bg-[#171717] transition-colors duration-300">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Welcome Back</h2>
        <p className="mt-2 max-w-sm text-sm text-gray-600 dark:text-gray-300">Login to Nyaysetu AI</p>

        {success && (
          <div className="mt-4 p-3 rounded-md bg-green-500/10 border border-green-500/50">
            <p className="text-sm text-green-500">{success}</p>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 rounded-md bg-red-500/10 border border-red-500/50">
            <p className="text-sm text-red-500">{error}</p>
          </div>
        )}

        <div className="my-6 space-y-4">


          {/* Google - Primary Option */}
          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={socialLoading === "google"}
            className="group/btn shadow-input relative flex h-12 w-full items-center justify-center space-x-3 rounded-md bg-gray-900 px-4 font-medium text-white hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <IconBrandGoogle className="h-5 w-5 text-white" />
            <span className="text-sm text-white">
              {socialLoading === "google" ? "Connecting..." : "Continue with Google"}
            </span>
            <BottomGradient />
          </button>


          {/* GitHub - Primary Option */}
          <button
            type="button"
            onClick={handleGitHubLogin}
            disabled={socialLoading === "github"}
            className="group/btn shadow-input relative flex h-12 w-full items-center justify-center space-x-3 rounded-md bg-gray-900 px-4 font-medium text-white hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <IconBrandGithub className="h-5 w-5 text-white" />
            <span className="text-sm text-white">
              {socialLoading === "github" ? "Connecting..." : "Continue with GitHub"}
            </span>
            <BottomGradient />
          </button>

          <div className="my-6 flex items-center">
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-600 to-transparent" />
            <span className="px-4 text-sm text-gray-500">or</span>
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-600 to-transparent" />
          </div>

          {/* Email Option - Expandable */}
          <button
            type="button"
            onClick={() => setShowEmailForm(!showEmailForm)}
            className="group/btn shadow-input relative flex h-12 w-full items-center justify-center space-x-3 rounded-md bg-transparent border border-gray-300 dark:border-gray-700 px-4 font-medium text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-900/50 transition-colors"
          >
            <IconMail className="h-5 w-5 text-gray-700 dark:text-white" />
            <span className="text-sm text-gray-700 dark:text-white">Continue with Email</span>
            {showEmailForm ? (
              <IconChevronUp className="h-4 w-4 text-gray-400 ml-auto" />
            ) : (
              <IconChevronDown className="h-4 w-4 text-gray-400 ml-auto" />
            )}
          </button>

          {/* Email Form - Collapsible */}
          <div className={cn(
            "overflow-hidden transition-all duration-300 ease-in-out",
            showEmailForm ? "max-h-[400px] opacity-100" : "max-h-0 opacity-0"
          )}>
            <form className="pt-4 space-y-4" onSubmit={handleSubmit}>
              <LabelInputContainer>
                <Label htmlFor="email" className="text-gray-700 dark:text-white">Email</Label>
                <Input
                  id="email"
                  placeholder="abc@gmail.com"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required={showEmailForm}
                  disabled={loading}
                  className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                />
              </LabelInputContainer>

              <LabelInputContainer>
                <Label htmlFor="password" className="text-gray-700 dark:text-white">Password</Label>
                <Input
                  id="password"
                  placeholder="••••••••"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  required={showEmailForm}
                  disabled={loading}
                  className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                />
              </LabelInputContainer>

              <button
                type="submit"
                disabled={loading}
                className="group/btn relative h-10 w-full rounded-md bg-black text-white font-medium shadow-[0px_1px_0px_0px_#00000040_inset,0px_-1px_0px_0px_#00000040_inset] transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Logging in..." : "Login with Email →"}
                <BottomGradient />
              </button>
            </form>
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 text-center pt-4">
            Don&apos;t have an account?{" "}
            <a href="/signup" className="text-cyan-600 dark:text-cyan-500 hover:underline">Sign up</a>
          </p>
        </div>
      </div>
    </div>
  );
}

const LoginPage = () => (
  <Suspense fallback={<div className="flex items-center justify-center min-h-screen bg-black"><div className="text-white">Loading...</div></div>}>
    <LoginForm />
  </Suspense>
);

const BottomGradient = () => (
  <>
    <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition-opacity duration-500 group-hover/btn:opacity-100" />
    <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition-opacity duration-500 group-hover/btn:opacity-100" />
  </>
);

const LabelInputContainer = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn("flex w-full flex-col space-y-2", className)}>{children}</div>
);

export default LoginPage;