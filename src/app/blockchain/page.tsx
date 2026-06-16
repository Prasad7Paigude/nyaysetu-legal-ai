"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import DashNavbar from "@/components/navbar/DashNavbar";
import { MagicCard } from "@/components/ui/magic-card";
import FooterComponent from "@/components/footer/FooterComponent";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface UploadedFile {
    filename: string;
    fileKey: string;
    secureName: string;
}

interface BlockchainTransaction {
    user: string;
    v_file: string;
    file_size: number;
    index: number;
    hash: string;
}

export default function BlockchainPage() {
    const router = useRouter();
    const { data: session, isPending } = authClient.useSession();

    const [userKey, setUserKey] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [myFiles, setMyFiles] = useState<UploadedFile[]>([]);
    const [sharedFiles, setSharedFiles] = useState<UploadedFile[]>([]); // New state for shared files
    const [transactions, setTransactions] = useState<BlockchainTransaction[]>([]);
    const [loading, setLoading] = useState(true);

    // Form states
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [senderKey, setSenderKey] = useState("");
    const [recipientKey, setRecipientKey] = useState("");
    const [sharingFileKey, setSharingFileKey] = useState("");
    const [viewingSharedFrom, setViewingSharedFrom] = useState(""); // Track whose files we're viewing
    const [viewingFileKey, setViewingFileKey] = useState<string | null>(null);

    const RENDER_BACKEND_URL = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";

    useEffect(() => {
        if (!isPending && !session) {
            router.push("/login");
            return;
        }

        if (session?.user?.email) {
            const user = session.user.email.split("@")[0];
            setUsername(user);

            // Get blockchain key from user data
            const bKey = (session.user as any).blockchainKey;
            if (bKey) {
                setUserKey(bKey);
                fetchUserFiles(bKey);
            }

            fetchBlockchainData();
        }
    }, [session, isPending, router]);

    const fetchUserFiles = async (key: string) => {
        try {
            const response = await fetch(`/api/blockchain/user-files?userKey=${key}`);
            if (response.ok) {
                const data = await response.json();
                setMyFiles(data.files || []);
            }
        } catch (error) {
            console.error("Error fetching files:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchBlockchainData = async () => {
        try {
            const response = await fetch('/api/blockchain/chain', {
                cache: 'no-store',
            });
            if (response.ok) {
                const data = await response.json();
                const txs: BlockchainTransaction[] = [];

                data.chain.forEach((block: any) => {
                    block.transactions.forEach((trans: any) => {
                        txs.push({
                            ...trans,
                            index: block.index,
                            hash: block.prev_hash,
                        });
                    });
                });

                setTransactions(txs.sort((a, b) => b.index - a.index));
            }
        } catch (error) {
            // Blockchain server not available - this is optional, so just log it
            console.log("Blockchain server not available:", error);
            setTransactions([]);
        }
    };

    const handleFileUpload = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!selectedFile || !username) {
            alert("Please select a file");
            return;
        }

        setUploading(true);

        try {
            const formData = new FormData();
            formData.append("v_file", selectedFile);
            formData.append("username", username);
            formData.append("userKey", userKey); // Pass the blockchain key from Next.js session

            const response = await fetch("/api/blockchain/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("File uploaded successfully!");
                setSelectedFile(null);
                // Reset file input
                const fileInput = document.getElementById("fileUpld") as HTMLInputElement;
                if (fileInput) fileInput.value = "";

                // Refresh files list
                await fetchUserFiles(userKey);
                await fetchBlockchainData();
            } else {
                const errorData = await response.json();
                alert("Upload failed: " + (errorData.error || "Unknown error"));
            }
        } catch (error) {
            console.error("Upload error:", error);
            alert("Upload failed. Make sure blockchain server is running on port 9000.");
        } finally {
            setUploading(false);
        }
    };

    const handleShareFile = async (fileKey: string, recipKey: string) => {
        if (!recipKey || !userKey) {
            alert("Please enter recipient key");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("file_key", fileKey);
            formData.append("recipient_key", recipKey);
            formData.append("userKey", userKey);

            const response = await fetch("/api/blockchain/share", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("File shared successfully!");
                setRecipientKey("");
                setSharingFileKey("");
            } else {
                alert("Failed to share file");
            }
        } catch (error) {
            console.error("Share error:", error);
            alert("Failed to share file");
        }
    };

    const handleViewShared = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!senderKey || !userKey) {
            alert("Please enter sender's key");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("sender_key", senderKey);
            formData.append("userKey", userKey);

            const response = await fetch("/api/blockchain/view-shared", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();

                if (data.files && data.files.length > 0) {
                    setSharedFiles(data.files);
                    setViewingSharedFrom(senderKey);
                } else {
                    setSharedFiles([]);
                    setViewingSharedFrom("");
                    alert("No files have been shared with you from this user");
                }
            } else {
                const error = await response.json();
                setSharedFiles([]);
                setViewingSharedFrom("");
                alert(error.error || "No files found");
            }
        } catch (error) {
            console.error("View shared error:", error);
            alert("Failed to view shared files");
        }
    };

    const handleDownload = (fileKey: string) => {
        // Direct download from Render backend (File Storage API)
        const downloadUrl = process.env.NEXT_PUBLIC_RENDER_BACKEND_URL || "http://127.0.0.1:9000";
        window.open(`${downloadUrl}/download/${fileKey}`, "_blank");
    };


    if (isPending || !session) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <p className="text-foreground text-lg">Loading...</p>
            </div>
        );
    }

    if (!userKey) {
        return (
            <>
                <DashNavbar />
                <div className="min-h-screen bg-background pt-24 px-4 pb-12 flex items-center justify-center">
                    <MagicCard className="w-full max-w-md bg-card p-8">
                        <h2 className="text-2xl font-bold text-foreground mb-4">Blockchain Key Not Found</h2>
                        <p className="text-muted-foreground mb-4">
                            Your blockchain key hasn't been generated yet. This usually happens during signup.
                        </p>
                        <Button onClick={() => router.push("/profile")} className="w-full">
                            Go to Profile
                        </Button>
                    </MagicCard>
                </div>
                <FooterComponent />
            </>
        );
    }

    return (
        <>
            <DashNavbar />

            <div className="min-h-screen bg-background pt-24 px-4 pb-12">
                <div className="max-w-7xl mx-auto">
                    {/* User Profile Section */}
                    <MagicCard className="w-full bg-card mb-6">
                        <div className="p-6">
                            <div>
                                <h2 className="text-2xl font-bold text-foreground mb-2">Welcome, {session.user.name?.split(" ")[0] || "User"}!</h2>
                                <p className="text-muted-foreground">
                                    Your Secret Key: <span className="font-mono text-foreground font-semibold">{userKey}</span>
                                </p>
                            </div>
                        </div>
                    </MagicCard>

                    {/* Main Content - 2 Columns */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Column 1: Upload and View Shared */}
                        <div className="space-y-6">
                            {/* Upload File */}
                            <MagicCard className="bg-card">
                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-foreground mb-4 text-center bg-primary/10 py-2 rounded">
                                        Upload a File
                                    </h3>
                                    <form onSubmit={handleFileUpload} className="space-y-4">
                                        <div>
                                            <Label htmlFor="fileUpld" className="text-foreground">Upload a File:</Label>
                                            <Input
                                                type="file"
                                                id="fileUpld"
                                                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                                                className="mt-2"
                                                required
                                            />
                                        </div>
                                        <Button type="submit" className="w-full bg-yellow-600 hover:bg-yellow-700 text-white" disabled={uploading}>
                                            {uploading ? "Uploading..." : "Upload"}
                                        </Button>
                                    </form>
                                </div>
                            </MagicCard>

                            {/* View Shared Files */}
                            <MagicCard className="bg-card">
                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-foreground mb-4 text-center bg-primary/10 py-2 rounded">
                                        View Shared Files
                                    </h3>
                                    <form onSubmit={handleViewShared} className="space-y-4">
                                        <div>
                                            <Label htmlFor="senderKey" className="text-foreground">
                                                Enter Sender's Secret Key:
                                            </Label>
                                            <Input
                                                type="text"
                                                id="senderKey"
                                                placeholder="Sender Key"
                                                value={senderKey}
                                                onChange={(e) => setSenderKey(e.target.value)}
                                                className="mt-2"
                                                required
                                            />
                                        </div>
                                        <Button type="submit" className="w-full bg-yellow-600 hover:bg-yellow-700 text-white">
                                            View Files
                                        </Button>
                                    </form>
                                </div>
                            </MagicCard>


                        </div>

                        {/* Column 2: My Files */}
                        <div>
                            {/* Shared Files Display */}
                            {sharedFiles.length > 0 && (
                                <MagicCard className="bg-card mb-6">
                                    <div className="p-6">
                                        <h3 className="text-xl font-bold text-foreground mb-4 text-center bg-primary/10 py-2 rounded">
                                            Shared Files
                                        </h3>
                                        <p className="text-sm text-muted-foreground mb-4 text-center">
                                            Files shared from: <span className="font-mono text-primary">{viewingSharedFrom.substring(0, 10)}...</span>
                                        </p>
                                        <div className="space-y-3 max-h-[400px] overflow-y-auto">
                                            {sharedFiles.map((file, index) => (
                                                <div key={index} className="border border-border rounded-lg p-4 bg-muted/30">
                                                    <div className="flex items-center justify-between">
                                                        <div>
                                                            <h5 className="font-semibold text-foreground mb-1">{file.filename}</h5>
                                                            <p className="text-xs text-muted-foreground">
                                                                File Key: {file.fileKey}
                                                            </p>
                                                        </div>
                                                        <div className="flex flex-col items-end gap-2">
                                                            <span className="text-[10px] font-bold uppercase tracking-wider text-primary bg-primary/10 px-2 py-0.5 rounded border border-primary/20">
                                                                View Only
                                                            </span>
                                                            <Button
                                                                onClick={() => setViewingFileKey(file.fileKey)}
                                                                size="sm"
                                                                className="bg-yellow-600 hover:bg-yellow-700 text-white"
                                                            >
                                                                View
                                                            </Button>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </MagicCard>
                            )}

                            <MagicCard className="bg-card">
                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-foreground mb-4 text-center bg-primary/10 py-2 rounded">
                                        My Files
                                    </h3>
                                    <div className="space-y-3 max-h-[600px] overflow-y-auto">
                                        {loading ? (
                                            <p className="text-center text-muted-foreground py-4">Loading...</p>
                                        ) : myFiles.length > 0 ? (
                                            myFiles.map((file) => (
                                                <div key={file.fileKey} className="border border-border rounded-lg p-4 bg-muted/30">
                                                    <div className="flex justify-between items-start mb-3">
                                                        <div>
                                                            <h5 className="font-semibold text-foreground mb-1">{file.filename}</h5>
                                                            <p className="text-xs text-muted-foreground">
                                                                File Key: {file.fileKey}
                                                            </p>
                                                        </div>
                                                        <div className="flex gap-2">
                                                            <Button
                                                                onClick={() => handleDownload(file.fileKey)}
                                                                size="sm"
                                                                variant="outline"
                                                                className="h-8"
                                                            >
                                                                Download
                                                            </Button>
                                                            <Button
                                                                onClick={() => setViewingFileKey(file.fileKey)}
                                                                size="sm"
                                                                className="bg-yellow-600 hover:bg-yellow-700 text-white h-8"
                                                            >
                                                                View
                                                            </Button>
                                                        </div>
                                                    </div>
                                                    <div className="flex gap-2">
                                                        <Input
                                                            type="text"
                                                            placeholder="Recipient Key"
                                                            value={sharingFileKey === file.fileKey ? recipientKey : ""}
                                                            onChange={(e) => {
                                                                setSharingFileKey(file.fileKey);
                                                                setRecipientKey(e.target.value);
                                                            }}
                                                            className="flex-1 h-9"
                                                        />
                                                        <Button
                                                            onClick={() => handleShareFile(file.fileKey, recipientKey)}
                                                            size="sm"
                                                            className="bg-yellow-600 hover:bg-yellow-700 text-white"
                                                        >
                                                            Share
                                                        </Button>
                                                    </div>
                                                </div>
                                            ))
                                        ) : (
                                            <p className="text-center text-muted-foreground py-8">No files uploaded yet.</p>
                                        )}
                                    </div>
                                </div>
                            </MagicCard>
                        </div>
                    </div>
                </div>
            </div>

            {/* File Viewer Modal */}
            {viewingFileKey && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
                    <div className="bg-background border border-border rounded-lg w-full h-full max-w-5xl max-h-[85vh] flex flex-col relative shadow-2xl">
                        <div className="flex justify-between items-center p-4 border-b border-border bg-card rounded-t-lg">
                            <h3 className="text-lg font-semibold text-foreground">File Preview</h3>
                            <div className="flex gap-2">
                                <Button
                                    onClick={() => window.open(`/api/blockchain/view?fileKey=${viewingFileKey}`, '_blank')}
                                    variant="outline"
                                    size="sm"
                                >
                                    Open in New Tab
                                </Button>
                                <Button
                                    onClick={() => setViewingFileKey(null)}
                                    variant="destructive"
                                    size="sm"
                                >
                                    Close
                                </Button>
                            </div>
                        </div>
                        <div className="flex-1 bg-muted p-1 overflow-hidden">
                            <iframe
                                src={`/api/blockchain/view?fileKey=${viewingFileKey}`}
                                className="w-full h-full rounded-b-lg border-none bg-white"
                                title="File Preview"
                            />
                        </div>
                    </div>
                </div>
            )}

            <FooterComponent />
        </>
    );
}
