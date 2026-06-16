import { NextResponse } from "next/server";

const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

export async function GET() {
    try {
        const response = await fetch(`${RENDER_BACKEND_URL}/chain`, {
            cache: 'no-store'
        });

        if (response.ok) {
            const data = await response.json();
            return NextResponse.json(data);
        } else {
            return NextResponse.json({ error: "Failed to fetch chain data" }, { status: response.status });
        }
    } catch (error) {
        console.error("Error fetching chain data:", error);
        return NextResponse.json(
            { error: "Failed to fetch chain data" },
            { status: 500 }
        );
    }
}
