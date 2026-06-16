
const fs = require("fs");
const { MongoClient } = require("mongodb");
require("dotenv").config({ path: ".env" });

async function dumpBlockchainUsers() {
    const uri = process.env.MONGODB_URI;
    const client = new MongoClient(uri);
    try {
        await client.connect();
        const db = client.db("file_storage");
        const users = await db.collection("users").find({}).toArray();

        let output = "Count: " + users.length + "\n";
        users.forEach(u => {
            output += `Username: ${u.username}, Key: ${u.key}, CreatedAt: ${u.createdAt}\n`;
        });

        fs.writeFileSync("blockchain_users_dump.txt", output);
    } catch (e) {
        fs.writeFileSync("blockchain_users_dump.txt", e.toString());
    } finally {
        await client.close();
    }
}

dumpBlockchainUsers();
