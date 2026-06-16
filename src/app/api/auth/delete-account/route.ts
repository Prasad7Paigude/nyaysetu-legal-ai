// app/api/auth/delete-account/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { MongoClient, ObjectId } from "mongodb";

export async function DELETE(req: NextRequest) {
    try {
        console.log("🔍 Delete account request received");

        // Get the current session
        const session = await auth.api.getSession({
            headers: await headers(),
        });

        console.log("Session:", session ? "Found" : "Not found");

        if (!session) {
            return NextResponse.json(
                { error: "Unauthorized" },
                { status: 401 }
            );
        }

        const userId = session.user.id;
        const userEmail = session.user.email;
        console.log("User ID to delete:", userId);
        console.log("User Email:", userEmail);

        // Connect to MongoDB and delete user data
        const client = new MongoClient(process.env.MONGODB_URI!);
        await client.connect();
        console.log("✅ Connected to MongoDB");

        const db = client.db(process.env.DB_NAME || "nyaysetu");

        // Delete user - try both id and _id fields
        const userResult1 = await db.collection("user").deleteOne({ id: userId });
        const userResult2 = await db.collection("user").deleteOne({ _id: new ObjectId(userId) });
        const userResult3 = await db.collection("user").deleteOne({ email: userEmail });
        console.log("User deleted by id:", userResult1.deletedCount);
        console.log("User deleted by _id:", userResult2.deletedCount);
        console.log("User deleted by email:", userResult3.deletedCount);

        // Delete sessions - try both userId and _id
        const sessionResult1 = await db.collection("session").deleteMany({ userId: userId });
        const sessionResult2 = await db.collection("session").deleteMany({ userId: new ObjectId(userId) });
        console.log("Sessions deleted by userId:", sessionResult1.deletedCount);
        console.log("Sessions deleted by ObjectId:", sessionResult2.deletedCount);

        // Delete accounts (OAuth connections) - try both userId and _id
        const accountResult1 = await db.collection("account").deleteMany({ userId: userId });
        const accountResult2 = await db.collection("account").deleteMany({ userId: new ObjectId(userId) });
        console.log("Accounts deleted by userId:", accountResult1.deletedCount);
        console.log("Accounts deleted by ObjectId:", accountResult2.deletedCount);

        // Delete verification records
        const verificationResult = await db.collection("verification").deleteMany({
            $or: [
                { identifier: userEmail },
                { email: userEmail }
            ]
        });
        console.log("Verifications deleted:", verificationResult.deletedCount);

        await client.close();
        console.log("✅ Account deletion completed successfully");

        return NextResponse.json(
            { message: "Account deleted successfully" },
            { status: 200 }
        );
    } catch (error: any) {
        console.error("❌ Error deleting account:", error);
        console.error("Error message:", error?.message);
        console.error("Error stack:", error?.stack);

        return NextResponse.json(
            {
                error: "Failed to delete account",
                details: error?.message || "Unknown error",
                stack: process.env.NODE_ENV === 'development' ? error?.stack : undefined
            },
            { status: 500 }
        );
    }
}
