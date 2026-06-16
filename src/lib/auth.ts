// lib/auth.ts
import { betterAuth } from "better-auth";
import { emailOTP } from "better-auth/plugins";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { MongoClient } from "mongodb";
import { Resend } from "resend";

const client = new MongoClient(process.env.MONGODB_URI!);
const db = client.db(process.env.DB_NAME || "nyaysetu");
export const resend = new Resend(process.env.RESEND_API_KEY);

export const auth = betterAuth({
  database: mongodbAdapter(db),
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  secret: process.env.BETTER_AUTH_SECRET,

  trustedOrigins: [
    "http://localhost:3000",
    "https://nyay-setu-prod.vercel.app",
  ],

  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },

  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    minPasswordLength: 6,
    autoSignIn: false,
  },

  user: {
    additionalFields: {
      firstName: { type: "string", required: false, input: true },
      lastName: { type: "string", required: false, input: true },
      blockchainKey: { type: "string", required: false, input: true },
    },
  },

  plugins: [
    emailOTP({
      otpLength: 6,
      expiresIn: 300,
      sendVerificationOnSignUp: true,
      async sendVerificationOTP({ email, otp, type }) {
        const subject =
          type === "email-verification"
            ? "Verify your email - Nyaysetu AI"
            : type === "sign-in"
              ? "Sign in OTP - Nyaysetu AI"
              : "Reset your password - Nyaysetu AI";

        const message =
          type === "email-verification"
            ? "Please use this code to verify your email address."
            : type === "sign-in"
              ? "Please use this code to sign in to your account."
              : "Please use this code to reset your password.";

        try {
          await resend.emails.send({
            from: "Nyaysetu AI <NyaysetuAI@shivrajtaware.in>",
            to: email,
            subject,
            html: `
              <body style="font-family:Arial;background:#000;padding:40px 20px;">
                <div style="max-width:500px;margin:0 auto;background:#171717;border-radius:16px;padding:40px;">
                  <h1 style="color:#0891b2;margin:0 0 10px;font-size:24px;">Nyaysetu AI</h1>
                  <p style="color:#d1d5db;margin:0 0 30px;font-size:14px;">${message}</p>
                  <div style="background:#000;border-radius:12px;padding:30px;text-align:center;margin:20px 0;">
                    <p style="color:#9ca3af;margin:0 0 10px;font-size:12px;text-transform:uppercase;">Your verification code</p>
                    <p style="color:#0891b2;font-size:36px;font-weight:bold;letter-spacing:8px;margin:0;">${otp}</p>
                  </div>
                  <p style="color:#6b7280;font-size:12px;margin:20px 0 0;">This code expires in 5 minutes.</p>
                </div>
              </body>
            `,
          });
          console.log(`✅ OTP sent to ${email}`);
        } catch (error) {
          console.error("❌ Failed to send OTP:", error);
          throw new Error("Failed to send verification email");
        }
      },
    }),
  ],
});

export type Session = typeof auth.$Infer.Session;