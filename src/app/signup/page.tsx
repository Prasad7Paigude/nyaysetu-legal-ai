// app/signup/page.tsx
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { IconBrandGithub, IconBrandGoogle, IconMail, IconChevronDown, IconChevronUp } from "@tabler/icons-react";
import { authClient } from "@/lib/auth-client";
import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler";

const SignupPage = () => {
  const router = useRouter();

  const [step, setStep] = useState<"signup" | "verify">("signup");
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  // ============================================
  // GITHUB SIGN UP
  // ============================================
  const handleGitHubSignUp = async () => {
    setError("");
    setSocialLoading("github");

    try {
      await authClient.signIn.social({
        provider: "github",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("GitHub signup error:", err);
      setError(err instanceof Error ? err.message : "GitHub signup failed");
      setSocialLoading(null);
    }
  };

  // ============================================
  // GOOGLE SIGN UP
  // ============================================
  const handleGoogleSignUp = async () => {
    setError("");
    setSocialLoading("google");

    try {
      await authClient.signIn.social({
        provider: "google",
        callbackURL: "/dashboard",
      });
    } catch (err) {
      console.error("Google signup error:", err);
      setError(err instanceof Error ? err.message : "Google signup failed");
      setSocialLoading(null);
    }
  };

  // ============================================
  // STEP 1: SIGNUP FORM SUBMISSION
  // ============================================
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      // Generate blockchain key first
      const blockchainKeyResponse = await fetch("/api/blockchain/generate-key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: formData.email }),
      });

      if (!blockchainKeyResponse.ok) {
        throw new Error("Failed to generate blockchain key");
      }

      const { blockchainKey } = await blockchainKeyResponse.json();

      // Sign up user with blockchain key
      const { data, error: signUpError } = await authClient.signUp.email({
        email: formData.email,
        password: formData.password,
        name: `${formData.firstName} ${formData.lastName}`,
      }, {
        body: {
          firstName: formData.firstName,
          lastName: formData.lastName,
          blockchainKey: blockchainKey,
        }
      });

      if (signUpError) {
        throw new Error(signUpError.message || "Signup failed");
      }

      console.log("Signup successful, blockchain key generated, moving to OTP verification");
      setStep("verify");

    } catch (err) {
      console.error("Signup error:", err);
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  // ============================================
  // STEP 2: OTP VERIFICATION
  // ============================================
  const handleVerifyOTP = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const { data, error: verifyError } = await authClient.emailOtp.verifyEmail({
        email: formData.email,
        otp: otp,
      });

      if (verifyError) {
        throw new Error(verifyError.message || "Verification failed");
      }

      console.log("Email verified successfully");
      window.location.href = "/login?verified=true";

    } catch (err) {
      console.error("OTP verification error:", err);
      setError(err instanceof Error ? err.message : "Invalid OTP");
    } finally {
      setLoading(false);
    }
  };

  // ============================================
  // RESEND OTP
  // ============================================
  const handleResendOTP = async () => {
    setError("");
    setLoading(true);

    try {
      const { error: resendError } = await authClient.emailOtp.sendVerificationOtp({
        email: formData.email,
        type: "email-verification",
      });

      if (resendError) {
        throw new Error(resendError.message);
      }

      alert("New OTP sent to your email!");

    } catch (err) {
      console.error("Resend OTP error:", err);
      setError(err instanceof Error ? err.message : "Failed to resend OTP");
    } finally {
      setLoading(false);
    }
  };

  // ============================================
  // RENDER: OTP VERIFICATION SCREEN
  // ============================================
  if (step === "verify") {
    return (
      <div className="flex items-center justify-center p-4 min-h-screen bg-gray-50 dark:bg-black transition-colors duration-300 relative">
        <div className="absolute top-4 right-4">
          <AnimatedThemeToggler />
        </div>
        <div className="shadow-input mx-auto w-full max-w-md rounded-2xl p-6 bg-white dark:bg-[#171717] transition-colors duration-300">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Verify Your Email</h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
            We sent a 6-digit code to{" "}
            <span className="text-cyan-600 dark:text-cyan-500">{formData.email}</span>
          </p>

          {error && <ErrorBox message={error} />}

          <form className="mt-6" onSubmit={handleVerifyOTP}>
            <LabelInputContainer className="mb-5">
              <Label htmlFor="otp" className="text-gray-700 dark:text-white">Enter OTP</Label>
              <Input
                id="otp"
                placeholder="123456"
                type="text"
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                required
                className="text-center text-2xl tracking-widest placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A] text-gray-900 dark:text-white"
              />
            </LabelInputContainer>

            <div className="flex flex-col items-center space-y-3">
              <button
                type="submit"
                disabled={loading || otp.length !== 6}
                className="group/btn relative h-10 w-44 rounded-md bg-black text-white font-medium shadow-[0px_1px_0px_0px_#00000040_inset,0px_-1px_0px_0px_#00000040_inset] transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Verifying..." : "Verify Email →"}
                <BottomGradient />
              </button>

              <button
                type="button"
                onClick={handleResendOTP}
                disabled={loading}
                className="text-sm text-cyan-600 dark:text-cyan-500 hover:underline disabled:opacity-50"
              >
                Did not receive code? Resend OTP
              </button>

              <button
                type="button"
                onClick={() => setStep("signup")}
                className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                ← Back to signup
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // ============================================
  // RENDER: SIGNUP FORM
  // ============================================
  return (
    <div className="flex items-center justify-center p-4 min-h-screen bg-gray-50 dark:bg-black transition-colors duration-300 relative">
      <div className="absolute top-4 right-4">
        <AnimatedThemeToggler />
      </div>
      <div className="shadow-input mx-auto w-full max-w-md rounded-2xl p-5 bg-white dark:bg-[#171717] transition-colors duration-300">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white">Welcome to Nyaysetu AI</h2>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">Create your account to get started</p>

        {error && <ErrorBox message={error} />}

        <div className="mt-5 space-y-3">

          {/* Google - Primary Option */}
          <button
            type="button"
            onClick={handleGoogleSignUp}
            disabled={socialLoading === "google"}
            className="group/btn shadow-input relative flex h-11 w-full items-center justify-center space-x-2 rounded-md bg-gray-900 px-4 font-medium text-white hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
            onClick={handleGitHubSignUp}
            disabled={socialLoading === "github"}
            className="group/btn shadow-input relative flex h-11 w-full items-center justify-center space-x-2 rounded-md bg-gray-900 px-4 font-medium text-white hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <IconBrandGithub className="h-5 w-5 text-white" />
            <span className="text-sm text-white">
              {socialLoading === "github" ? "Connecting..." : "Continue with GitHub"}
            </span>
            <BottomGradient />
          </button>

          {/* Divider */}
          <div className="flex items-center py-1">
            <div className="h-[1px] flex-1 bg-gray-300 dark:bg-gray-700" />
            <span className="px-3 text-xs text-gray-500">or</span>
            <div className="h-[1px] flex-1 bg-gray-300 dark:bg-gray-700" />
          </div>

          {/* Email Option - Expandable */}
          <button
            type="button"
            onClick={() => setShowEmailForm(!showEmailForm)}
            className="group/btn shadow-input relative flex h-11 w-full items-center justify-center space-x-2 rounded-md bg-transparent border border-gray-300 dark:border-gray-700 px-4 font-medium text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-900/50 transition-colors"
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
            showEmailForm ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"
          )}>
            <form className="pt-3 space-y-2.5" onSubmit={handleSubmit}>
              {/* First & Last Name - Side by Side */}
              <div className="flex space-x-2">
                <LabelInputContainer>
                  <Label htmlFor="firstName" className="text-gray-700 dark:text-white text-xs">First name</Label>
                  <Input
                    id="firstName"
                    placeholder="Shivraj"
                    type="text"
                    value={formData.firstName}
                    onChange={handleChange}
                    required={showEmailForm}
                    className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 h-9 text-sm bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                  />
                </LabelInputContainer>

                <LabelInputContainer>
                  <Label htmlFor="lastName" className="text-gray-700 dark:text-white text-xs">Last name</Label>
                  <Input
                    id="lastName"
                    placeholder="Taware"
                    type="text"
                    value={formData.lastName}
                    onChange={handleChange}
                    required={showEmailForm}
                    className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 h-9 text-sm bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                  />
                </LabelInputContainer>
              </div>

              {/* Email */}
              <LabelInputContainer>
                <Label htmlFor="email" className="text-gray-700 dark:text-white text-xs">Email Address</Label>
                <Input
                  id="email"
                  placeholder="abc@gmail.com"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required={showEmailForm}
                  className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 h-9 text-sm bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                />
              </LabelInputContainer>

              {/* Password & Confirm - Side by Side */}
              <div className="flex space-x-2">
                <LabelInputContainer>
                  <Label htmlFor="password" className="text-gray-700 dark:text-white text-xs">Password</Label>
                  <Input
                    id="password"
                    placeholder="••••••••"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    required={showEmailForm}
                    className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 h-9 text-sm bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                  />
                </LabelInputContainer>

                <LabelInputContainer>
                  <Label htmlFor="confirmPassword" className="text-gray-700 dark:text-white text-xs">Confirm</Label>
                  <Input
                    id="confirmPassword"
                    placeholder="••••••••"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required={showEmailForm}
                    className="text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 border rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 h-9 text-sm bg-white dark:bg-[#171717] border-gray-300 dark:border-[#3A3A3A]"
                  />
                </LabelInputContainer>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="group/btn relative h-9 w-full rounded-md bg-black text-white text-sm font-medium shadow-[0px_1px_0px_0px_#00000040_inset,0px_-1px_0px_0px_#00000040_inset] transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed mt-1"
              >
                {loading ? "Signing up..." : "Sign up with Email →"}
                <BottomGradient />
              </button>
            </form>
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 text-center pt-2">
            Already have an account?{" "}
            <a href="/login" className="text-cyan-600 dark:text-cyan-500 hover:underline">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
};

// ============================================
// HELPER COMPONENTS
// ============================================
const BottomGradient = () => (
  <>
    <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
    <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
  </>
);

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => (
  <div className={cn("flex w-full flex-col space-y-1", className)}>{children}</div>
);

const ErrorBox = ({ message }: { message: string }) => (
  <div className="mt-3 p-2 rounded-md bg-red-500/10 border border-red-500/50">
    <p className="text-sm text-red-500">{message}</p>
  </div>
);

export default SignupPage;