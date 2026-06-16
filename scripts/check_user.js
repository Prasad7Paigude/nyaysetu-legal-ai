
const fs = require("fs");
const { MongoClient } = require("mongodb");
require("dotenv").config({ path: ".env" });

async function checkUserStructure() {
    const uri = process.env.MONGODB_URI;
    const client = new MongoClient(uri);
    try {
        await client.connect();
        const dbName = process.env.DB_NAME || "nyaysetu";
        const db = client.db(dbName);
        const user = await db.collection("user").findOne({});

        let output = "";
        output += "Sample User Document Keys: " + JSON.stringify(Object.keys(user || {})) + "\n";
        if (user) {
            output += "ID Type: " + typeof user._id + "\n";
            output += "Has 'id' field?: " + (user.id !== undefined) + "\n";
            output += "Sample _id: " + user._id.toString() + "\n";
            output += "Sample id: " + user.id + "\n";
        } else {
            output += "No users found.\n";
        }
        fs.writeFileSync("check_user_output.txt", output);
    } catch (e) {
        fs.writeFileSync("check_user_output.txt", e.toString());
    } finally {
        await client.close();
    }
}

checkUserStructure();
