// API route for newsletter subscription
import { NextRequest, NextResponse } from "next/server";
import { MongoClient } from "mongodb";
import { auth } from "@/lib/auth";

const MONGODB_URI = process.env.MONGODB_URI!;
const DB_NAME = process.env.DB_NAME || "nyaysetu";

export async function POST(req: NextRequest) {
    try {
        // Get authenticated session
        const session = await auth.api.getSession({ headers: req.headers });

        if (!session) {
            return NextResponse.json(
                { error: "Unauthorized. Please log in first." },
                { status: 401 }
            );
        }

        const { email } = await req.json();

        // Validate email is provided
        if (!email || !email.trim()) {
            return NextResponse.json(
                { error: "Email is required" },
                { status: 400 }
            );
        }

        // Validate email matches user's account email
        if (email.toLowerCase() !== session.user.email.toLowerCase()) {
            return NextResponse.json(
                {
                    error: "Please use the same email you used to create your account.",
                    userEmail: session.user.email
                },
                { status: 400 }
            );
        }

        // Connect to MongoDB
        const client = new MongoClient(MONGODB_URI);
        await client.connect();

        const db = client.db(DB_NAME);
        const usersCollection = db.collection("user");

        // Update user with newsletter subscription using email to find user
        const result = await usersCollection.updateOne(
            { email: session.user.email },
            {
                $set: {
                    newsletterSubscription: {
                        status: "active",
                        subscribedAt: new Date(),
                    }
                }
            }
        );

        await client.close();

        if (result.matchedCount === 0) {
            return NextResponse.json(
                { error: "User not found" },
                { status: 404 }
            );
        }

        // --- Post-subscription Actions (Run in parallel for speed) ---

        const resend = (await import("@/lib/auth")).resend;
        const webhookUrl = process.env.NEWSLETTER_SHEET_WEBHOOK_URL;

        // Define the actions
        const sendEmail = async () => {
            try {
                await resend.emails.send({
                    from: "Nyaysetu AI <NyaysetuAI@shivrajtaware.in>",
                    to: session.user.email,
                    subject: "Welcome to NyaySetu Legal Brief!",
                    html: `
                        <body style="font-family:Arial,sans-serif;background:#000;padding:40px 20px;">
                            <div style="max-width:600px;margin:0 auto;background:#171717;border-radius:16px;padding:40px;color:#d1d5db;">
                                <h1 style="color:#0891b2;margin:0 0 20px;font-size:28px;">Welcome to NyaySetu!</h1>
                                <p style="font-size:16px;line-height:1.6;margin-bottom:20px;">
                                    Hello ${session.user.name || 'there'},
                                </p>
                                <p style="font-size:16px;line-height:1.6;margin-bottom:20px;">
                                    Thank you for subscribing to the NyaySetu Legal Brief. You're now part of a community dedicated to legal awareness and digital justice.
                                </p>
                                <div style="background:#000;border-radius:12px;padding:25px;margin:30px 0;border:1px solid #333;">
                                    <h2 style="color:#0891b2;font-size:18px;margin-top:0;">What to expect:</h2>
                                    <ul style="padding-left:20px;margin:0;">
                                        <li style="margin-bottom:10px;">Weekly legal insights curated by AI</li>
                                        <li style="margin-bottom:10px;">Summaries of landmark judgments</li>
                                        <li style="margin-bottom:10px;">Practical guides on your legal rights</li>
                                    </ul>
                                </div>
                                <p style="font-size:14px;color:#6b7280;margin-top:30px;border-top:1px solid #333;padding-top:20px;">
                                    Stay informed, stay empowered.<br>
                                    <strong>The NyaySetu Team</strong>
                                </p>
                            </div>
                        </body>
                    `,
                });
                return "Sent";
            } catch (error) {
                console.error("❌ Failed to send welcome email:", error);
                return "Failed";
            }
        };

        const updateSheet = async (mailStatus: string) => {
            if (!webhookUrl) {
                return;
            }

            if (webhookUrl.includes("docs.google.com/spreadsheets")) {
                console.error("❌ ERROR: NEWSLETTER_SHEET_WEBHOOK_URL is set to a Google Sheet URL, but it MUST be a Google Apps Script Web App URL (ending in /exec).");
                return;
            }

            try {
                const sheetResponse = await fetch(webhookUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        email: session.user.email,
                        status: "active",
                        mailSent: mailStatus
                    }),
                });
                if (sheetResponse.ok) {
                } else {
                    console.error(`❌ Google Sheets webhook returned status ${sheetResponse.status}. (Ensure you used the Apps Script /exec URL, not the Sheet URL)`);
                }
            } catch (error) {
                console.error("❌ Failed to update Google Sheets:", error);
            }
        };

        // Fire and forget or await all (awaiting ensures they complete before response)
        const emailStatus = await sendEmail();
        await updateSheet(emailStatus);

        return NextResponse.json({
            success: true,
            message: "Successfully subscribed to newsletter!",
        });

    } catch (error) {
        console.error("Newsletter subscription error:", error);
        return NextResponse.json(
            { error: "Failed to subscribe to newsletter" },
            { status: 500 }
        );
    }
}
