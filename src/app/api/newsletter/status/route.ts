// API route to get newsletter subscription status
import { NextRequest, NextResponse } from "next/server";
import { MongoClient } from "mongodb";
import { auth } from "@/lib/auth";

const MONGODB_URI = process.env.MONGODB_URI!;
const DB_NAME = process.env.DB_NAME || "nyaysetu";

export async function GET(req: NextRequest) {
    try {
        // Get authenticated session
        const session = await auth.api.getSession({ headers: req.headers });

        if (!session) {
            return NextResponse.json(
                { subscribed: false },
                { status: 200 }
            );
        }

        // Connect to MongoDB
        const client = new MongoClient(MONGODB_URI);
        await client.connect();

        const db = client.db(DB_NAME);
        const usersCollection = db.collection("user");

        // Get user's newsletter subscription status using email
        const user = await usersCollection.findOne(
            { email: session.user.email },
            { projection: { newsletterSubscription: 1 } }
        );

        await client.close();

        const isSubscribed = user?.newsletterSubscription?.status === "active";

        return NextResponse.json({
            subscribed: isSubscribed,
            status: user?.newsletterSubscription?.status || null,
        });

    } catch (error) {
        console.error("Newsletter status check error:", error);
        return NextResponse.json(
            { subscribed: false },
            { status: 200 }
        );
    }
}
