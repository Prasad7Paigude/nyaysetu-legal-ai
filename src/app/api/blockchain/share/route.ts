import { NextRequest, NextResponse } from "next/server";

const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const fileKey = formData.get("file_key") as string;
        const recipientKey = formData.get("recipient_key") as string;
        const userKey = formData.get("userKey") as string;

        if (!fileKey || !recipientKey || !userKey) {
            return NextResponse.json({ error: "file_key, recipient_key, and userKey are required" }, { status: 400 });
        }

        // Call Flask backend with keys
        const backendForm = new FormData();
        backendForm.append("file_key", fileKey);
        backendForm.append("recipient_key", recipientKey);
        backendForm.append("userKey", userKey);

        const response = await fetch(`${RENDER_BACKEND_URL}/share`, {
            method: "POST",
            body: backendForm,
        });

        if (response.ok) {
            const data = await response.json();
            return NextResponse.json(data, { status: 200 });
        } else {
            const error = await response.json();
            return NextResponse.json({ error: error.error || "Failed to share file" }, { status: response.status });
        }
    } catch (error) {
        console.error("Error sharing file:", error);
        return NextResponse.json(
            { error: "Failed to share file" },
            { status: 500 }
        );
    }
}
