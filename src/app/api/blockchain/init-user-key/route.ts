import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";
import { MongoClient, ObjectId } from "mongodb";
import { v4 as uuidv4 } from "uuid";

export async function POST(req: NextRequest) {
    try {
        const session = await auth.api.getSession({
            headers: req.headers,
        });

        if (!session || !session.user) {
            return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
        }

        const user = session.user as any;

        // If user already has a key, return it
        if (user.blockchainKey) {
            return NextResponse.json({ blockchainKey: user.blockchainKey });
        }

        const newKey = uuidv4();
        const email = user.email;
        const username = email.split("@")[0];

        // Connect to MongoDB
        const client = new MongoClient(process.env.MONGODB_URI!);
        await client.connect();

        try {
            // 1. Update Auth Database (user record)
            const authDb = client.db(process.env.DB_NAME || "nyaysetu");
            // Better-auth default collection is "user"
            // FIX: Use _id as ObjectId because MongoDB documents use _id, not id string
            const updateResult = await authDb.collection("user").updateOne(
                { _id: new ObjectId(user.id) },
                { $set: { blockchainKey: newKey } }
            );

            // 2. Sync with Blockchain Database
            const bcDb = client.db("file_storage");
            const bcUsers = bcDb.collection("users");

            // Check if user already exists in blockchain DB by username OR by full email
            // (Handling legacy cases where full email was stored as username)
            const existingBcUser = await bcUsers.findOne({
                $or: [
                    { username: username },
                    { username: email }
                ]
            });

            let finalKey = newKey;

            if (existingBcUser) {
                // If they exist in BC DB, use THAT key instead to maintain consistency
                console.log(`[DEBUG] Found existing BC user for ${username}. Key: ${existingBcUser.key}`);
                finalKey = existingBcUser.key;

                // Update Auth DB with the existing BC key
                const syncResult = await authDb.collection("user").updateOne(
                    { _id: new ObjectId(user.id) },
                    { $set: { blockchainKey: finalKey } }
                );
                console.log(`[DEBUG] Synced existing key to Auth DB. Modified: ${syncResult.modifiedCount}`);
            } else {
                // Otherwise create new entry in BC DB
                console.log(`[DEBUG] Creating NEW BC user for ${username} with key ${newKey}`);
                await bcUsers.insertOne({
                    username,
                    key: finalKey,
                    createdAt: new Date(),
                });
            }

            return NextResponse.json({ blockchainKey: finalKey });
        } finally {
            await client.close();
        }
    } catch (error) {
        console.error("Error initializing blockchain key:", error);
        return NextResponse.json(
            { error: "Failed to initialize blockchain key" },
            { status: 500 }
        );
    }
}
