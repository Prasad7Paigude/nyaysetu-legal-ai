
const { MongoClient } = require("mongodb");
require("dotenv").config({ path: ".env" });

async function listCollections() {
    const uri = process.env.MONGODB_URI;
    if (!uri) {
        console.error("MONGODB_URI not found");
        return;
    }
    const client = new MongoClient(uri);
    try {
        await client.connect();
        const dbName = process.env.DB_NAME || "nyaysetu";
        const db = client.db(dbName);
        const collections = await db.listCollections().toArray();
        console.log("Collections in " + dbName + ":");
        collections.forEach(c => console.log("- " + c.name));
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

listCollections();
