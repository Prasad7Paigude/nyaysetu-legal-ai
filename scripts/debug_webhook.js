
const fs = require('fs');
const https = require('https');
const path = require('path');

try {
    const envPath = path.join(__dirname, '.env');
    const envContent = fs.readFileSync(envPath, 'utf8');
    const match = envContent.match(/NEWSLETTER_SHEET_WEBHOOK_URL=(.*)/);

    if (!match) {
        console.log("ERROR: NEWSLETTER_SHEET_WEBHOOK_URL not found in .env");
        process.exit(1);
    }

    let url = match[1].trim();
    // Remove quotes if present
    if (url.startsWith('"') && url.endsWith('"')) {
        url = url.slice(1, -1);
    }

    console.log(`Found URL in .env: ${url}`);

    const data = JSON.stringify({
        email: "debug_test@example.com",
        status: "active",
        mailSent: "Sent"
    });

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    console.log("Sending test request...");

    const req = https.request(url, options, (res) => {
        console.log(`Response Status: ${res.statusCode}`);
        if (res.statusCode === 403) {
            console.log("❌ Forbidden (403): The script permissions are still restricted.");
        } else if (res.statusCode === 302) {
            console.log("⚠️ Redirect (302): Google Script is redirecting. This is usually okay for browsers but standard fetch/axios follow redirects automatically.");
            console.log("Redirect location:", res.headers.location);
        } else if (res.statusCode === 200) {
            console.log("✅ Success (200): The webhook is working!");
        }

        res.on('data', d => process.stdout.write(d));
    });

    req.on('error', (e) => {
        console.error(`Problem with request: ${e.message}`);
    });

    req.write(data);
    req.end();

} catch (err) {
    console.error("Error reading .env:", err.message);
}
