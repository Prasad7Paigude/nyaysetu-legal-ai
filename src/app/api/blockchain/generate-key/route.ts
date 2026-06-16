import { NextRequest, NextResponse } from "next/server";
import { MongoClient } from "mongodb";
import { v4 as uuidv4 } from "uuid";

const MONGODB_URI = process.env.MONGODB_URI!;
const BLOCKCHAIN_DB_NAME = "file_storage"; // Blockchain database name

export async function POST(req: NextRequest) {
    try {
        const { email } = await req.json();

        if (!email) {
            return NextResponse.json({ error: "Email is required" }, { status: 400 });
        }

        // Extract username from email (part before @)
        const username = email.split("@")[0];

        // Generate blockchain secret key
        const blockchainKey = uuidv4();

        // Connect to MongoDB
        const client = new MongoClient(MONGODB_URI);
        await client.connect();

        try {
            // Access blockchain database
            const db = client.db(BLOCKCHAIN_DB_NAME);
            const usersCollection = db.collection("users");

            // Check if user already exists
            const existingUser = await usersCollection.findOne({ username });

            if (existingUser) {
                // Return existing key
                return NextResponse.json({
                    blockchainKey: existingUser.key,
                    existed: true,
                });
            }

            // Create new user in blockchain database
            await usersCollection.insertOne({
                username,
                key: blockchainKey,
                createdAt: new Date(),
            });

            return NextResponse.json({
                blockchainKey,
                existed: false,
            });
        } finally {
            await client.close();
        }
    } catch (error) {
        console.error("Error generating blockchain key:", error);
        return NextResponse.json(
            { error: "Failed to generate blockchain key" },
            { status: 500 }
        );
    }
}
