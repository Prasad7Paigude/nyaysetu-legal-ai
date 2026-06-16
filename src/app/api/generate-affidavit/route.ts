import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
    try {
        const data = await req.json();

        // Validate required fields
        const requiredFields = ['name', 'father_name', 'mother_name', 'address'];
        const missingFields = requiredFields.filter(field => !data[field]);

        if (missingFields.length > 0) {
            return NextResponse.json(
                { error: 'Missing required fields', missingFields },
                { status: 400 }
            );
        }

        // Call the Render API
        const renderApiUrl = process.env.AFFIDAVIT_API_URL || 'http://localhost:5000';

        const response = await fetch(`${renderApiUrl}/api/generate-affidavit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            let errorDetail = 'Unknown error';
            try {
                const errorData = await response.json();
                errorDetail = errorData.error || errorData.message || errorDetail;
            } catch (e) {
                // If not JSON, get the text body
                const textError = await response.text().catch(() => '');
                console.error('Backend returned non-JSON error:', textError);
                errorDetail = `Backend Error (${response.status}): ${textError.slice(0, 100)}${textError.length > 100 ? '...' : ''}`;
            }

            return NextResponse.json(
                { error: errorDetail },
                { status: response.status }
            );
        }

        // Get the PDF as a blob
        const pdfBlob = await response.blob();

        // Return the PDF with proper headers
        return new NextResponse(pdfBlob, {
            status: 200,
            headers: {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename="NyaySetu_Affidavit.pdf"',
            },
        });

    } catch (error) {
        console.error('Error generating affidavit:', error);
        return NextResponse.json(
            { error: 'Internal server error', message: (error as Error).message },
            { status: 500 }
        );
    }
}
