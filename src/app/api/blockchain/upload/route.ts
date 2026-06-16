import { NextRequest, NextResponse } from "next/server";

const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const file = formData.get("v_file") as File;
        const username = formData.get("username") as string;
        const userKey = formData.get("userKey") as string;

        if (!file || !username || !userKey) {
            return NextResponse.json({ error: "Missing file, username, or userKey" }, { status: 400 });
        }

        // Upload file directly to Flask with userKey
        const uploadForm = new FormData();
        uploadForm.append("v_file", file);
        uploadForm.append("userKey", userKey);

        const uploadResponse = await fetch(`${RENDER_BACKEND_URL}/submit`, {
            method: "POST",
            body: uploadForm,
        });

        // Flask redirects on success (status 302)
        if (uploadResponse.ok || uploadResponse.status === 302) {
            return NextResponse.json({ success: true, message: "File uploaded successfully" });
        } else {
            const errorText = await uploadResponse.text();
            console.error("Upload failed:", errorText.substring(0, 500));
            return NextResponse.json({
                error: "Upload failed. Please ensure blockchain server is running."
            }, { status: uploadResponse.status });
        }
    } catch (error: any) {
        console.error("Upload error:", error);
        return NextResponse.json(
            { error: "Failed to upload file: " + (error.message || "Network error") },
            { status: 500 }
        );
    }
}
