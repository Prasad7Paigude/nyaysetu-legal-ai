// API route for newsletter unsubscribe
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

        // Connect to MongoDB
        const client = new MongoClient(MONGODB_URI);
        await client.connect();

        const db = client.db(DB_NAME);
        const usersCollection = db.collection("user");

        // Update user newsletter subscription to inactive using email
        const result = await usersCollection.updateOne(
            { email: session.user.email },
            {
                $set: {
                    "newsletterSubscription.status": "inactive",
                    "newsletterSubscription.unsubscribedAt": new Date(),
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

        // --- Post-unsubscribe Actions ---

        const webhookUrl = process.env.NEWSLETTER_SHEET_WEBHOOK_URL;

        // Call Google Sheets Webhook to set status to inactive
        if (webhookUrl) {
            if (webhookUrl.includes("docs.google.com/spreadsheets")) {
                console.error("❌ ERROR: NEWSLETTER_SHEET_WEBHOOK_URL is set to a Google Sheet URL, but it MUST be a Google Apps Script Web App URL (ending in /exec).");
            } else {
                try {
                    const sheetResponse = await fetch(webhookUrl, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            email: session.user.email,
                            status: "inactive",
                            mailSent: "N/A"
                        }),
                    });

                    if (sheetResponse.ok) {
                        console.log(`✅ Google Sheets updated (inactive) for ${session.user.email}`);
                    } else {
                        console.error(`❌ Google Sheets webhook returned status ${sheetResponse.status}. (Ensure you used the Apps Script /exec URL, not the Sheet URL)`);
                    }
                } catch (error) {
                    console.error("❌ Failed to update Google Sheets:", error);
                }
            }
        } else {
            console.warn("⚠️ NEWSLETTER_SHEET_WEBHOOK_URL is not defined in environment variables. Google Sheets sync skipped.");
        }

        return NextResponse.json({
            success: true,
            message: "Successfully unsubscribed from newsletter",
        });

    } catch (error) {
        console.error("Newsletter unsubscribe error:", error);
        return NextResponse.json(
            { error: "Failed to unsubscribe from newsletter" },
            { status: 500 }
        );
    }
}
