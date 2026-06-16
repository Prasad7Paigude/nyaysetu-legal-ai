import { NextRequest, NextResponse } from "next/server";

const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

export async function GET(req: NextRequest) {
    const searchParams = req.nextUrl.searchParams;
    const fileKey = searchParams.get("fileKey");

    if (!fileKey) {
        return NextResponse.json({ error: "Missing fileKey" }, { status: 400 });
        return new NextResponse(
            `<html><body><h2>Bad Request</h2><p>Missing 'fileKey' parameter.</p></body></html>`,
            { status: 400, headers: { 'Content-Type': 'text/html' } }
        );
    }

    try {
        const response = await fetch(`${RENDER_BACKEND_URL}/download/${fileKey}`);

        if (!response.ok) {
            console.error(`Backend returned ${response.status} for fileKey: ${fileKey}`);
            return new NextResponse(
                `<html><body><h2>File not found</h2><p>Backend returned status: ${response.status}</p></body></html>`,
                { status: response.status, headers: { 'Content-Type': 'text/html' } }
            );
        }

        const headers = new Headers();

        // Copy specific headers we want to pass through
        const contentType = response.headers.get("Content-Type");
        const contentLength = response.headers.get("Content-Length");

        if (contentType) headers.set("Content-Type", contentType);
        if (contentLength) headers.set("Content-Length", contentLength);

        // Force inline display with filename if available
        headers.set("Content-Disposition", "inline");

        return new NextResponse(response.body, {
            status: 200,
            headers: headers,
        });
    } catch (error: any) {
        console.error("View error:", error);
        return new NextResponse(
            `<html><body><h2>Error loading file</h2><p>Details: ${error.message}</p><p>Is the backend running at ${RENDER_BACKEND_URL}?</p></body></html>`,
            { status: 500, headers: { 'Content-Type': 'text/html' } }
        );
    }
}
