// app/api/chat/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { message, history } = await req.json();

    if (!message || typeof message !== "string") {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    const apiUrl = process.env.PYTHON_API_URL || "http://127.0.0.1:5000/chat";

    const sanitizedHistory = Array.isArray(history) ? history.map((msg: any) => ({
      text: msg.text,
      sender: msg.sender
    })) : [];

    const requestBody = {
      message: message,
      history: sanitizedHistory,
    };

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
        signal: AbortSignal.timeout(60000) // 60 second timeout
      });

      if (!response.ok) {
        if (response.status === 502 || response.status === 504) {
          return NextResponse.json({
            response: "The AI system is currently warming up or restarting. This may take up to 2-3 minutes. Please try again shortly.",
            error: "Service Temporarily Unavailable"
          });
        }

        const errorText = await response.text();
        console.error(`Python API error: ${response.status} ${response.statusText}`, errorText);
        throw new Error(`Backend responded with ${response.status}: ${errorText || response.statusText}`);
      }

      const data = await response.json();

      return NextResponse.json({
        response: data.reply || data.response || data.message || data.answer || "I'm not sure how to respond to that.",
      });
    } catch (error: any) {
      console.error("Chat API error:", error);

      // Return the actual error message for debugging
      return NextResponse.json({
        error: "Internal Server Error",
        details: error.message,
        response: `Error: ${error.message}. Please check server logs.`,
      }, { status: 500 });
    }
  } catch (error: any) { // Top level catch for request parsing errors
    console.error("Request parsing error:", error);
    return NextResponse.json({
      error: "Bad Request",
      response: "Invalid request format."
    }, { status: 400 });
  }
}