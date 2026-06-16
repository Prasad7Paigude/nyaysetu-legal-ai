import { NextRequest, NextResponse } from "next/server";
import { MongoClient } from "mongodb";

const MONGODB_URI = process.env.MONGODB_URI!;
const BLOCKCHAIN_DB_NAME = "file_storage";

export async function GET(req: NextRequest) {
    try {
        const { searchParams } = new URL(req.url);
        const userKey = searchParams.get("userKey");

        if (!userKey) {
            return NextResponse.json({ error: "User key is required" }, { status: 400 });
        }

        const client = new MongoClient(MONGODB_URI);
        await client.connect();

        try {
            const db = client.db(BLOCKCHAIN_DB_NAME);
            const filesCollection = db.collection("files");

            // Find files owned by this user
            console.log(`Fetching files for userKey: ${userKey}`);
            console.log(`Using DB: ${BLOCKCHAIN_DB_NAME}, Collection: files`);

            const files = await filesCollection
                .find({ owner: userKey })
                .toArray();

            console.log(`Found ${files.length} files`);
            if (files.length > 0) {
                console.log("First file sample:", files[0]);
            }

            const userFiles = files.map((f) => ({
                filename: f.filename,
                fileKey: f.file_key,
                secureName: f.secure_name,
            }));

            return NextResponse.json({ files: userFiles });
        } finally {
            await client.close();
        }
    } catch (error) {
        console.error("Error fetching user files:", error);
        return NextResponse.json(
            { error: "Failed to fetch files" },
            { status: 500 }
        );
    }
}
