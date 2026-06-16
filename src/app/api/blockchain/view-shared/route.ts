import { NextRequest, NextResponse } from "next/server";

const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const senderKey = formData.get("sender_key") as string;
        const userKey = formData.get("userKey") as string;

        if (!senderKey || !userKey) {
            return NextResponse.json({ error: "sender_key and userKey are required" }, { status: 400 });
        }

        // Call Flask backend with keys
        const backendForm = new FormData();
        backendForm.append("sender_key", senderKey);
        backendForm.append("userKey", userKey);

        const response = await fetch(`${RENDER_BACKEND_URL}/view_shared`, {
            method: "POST",
            body: backendForm,
        });

        if (response.ok) {
            const data = await response.json();

            // Map backend keys to frontend keys
            const mappedFiles = (data.files || []).map((f: any) => ({
                filename: f.filename,
                fileKey: f.file_key,
                secureName: f.secure_name,
            }));

            return NextResponse.json({ files: mappedFiles }, { status: 200 });
        } else {
            const error = await response.json().catch(() => ({}));
            return NextResponse.json({ error: error.error || "Failed to fetch shared files" }, { status: response.status });
        }
    } catch (error) {
        console.error("Error viewing shared files:", error);
        return NextResponse.json(
            { error: "Failed to view shared files" },
            { status: 500 }
        );
    }
}
