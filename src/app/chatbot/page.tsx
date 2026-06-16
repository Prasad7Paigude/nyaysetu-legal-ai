"use client";
import React, { useState, useRef } from "react";
import DashNavbar from "@/components/navbar/DashNavbar";
import { IconSend, IconUser, IconRobot, IconPaperclip, IconMicrophone, IconX, IconFileText, IconPhoto } from "@tabler/icons-react";
import { MagicCard } from "@/components/ui/magic-card";
import FooterComponent from "@/components/footer/FooterComponent";

interface Message {
  id: string;
  text: string;
  sender: "user" | "ai";
  timestamp: Date;
  attachment?: {
    name: string;
    type: "image" | "file";
    url?: string;
  };
}

const ChatbotPage = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your legal AI assistant. How can I help you today?",
      sender: "ai",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if ((!input.trim() && !selectedFile) || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input.trim(),
      sender: "user",
      timestamp: new Date(),
      attachment: selectedFile ? {
        name: selectedFile.name,
        type: selectedFile.type.startsWith("image/") ? "image" : "file",
        url: URL.createObjectURL(selectedFile) // Create temporary URL for preview
      } : undefined
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    setLoading(true);

    try {
      // Directly call the Render server API endpoint
      const renderApiUrl = "https://vois-nyaysetu-chatbot.onrender.com/chat";

      // Sanitize history to send only necessary fields
      const sanitizedHistory = messages.slice(-5).map(msg => ({
        text: msg.text,
        sender: msg.sender
      }));

      const response = await fetch(renderApiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.text,
          history: sanitizedHistory,
        }),
        signal: AbortSignal.timeout(60000), // 60 second timeout
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle Cold Start / Timeout (502 Bad Gateway / 504 Gateway Timeout)
        if (response.status === 502 || response.status === 504) {
          throw new Error("The AI system is warming up. This may take 2-3 minutes. Please try again shortly.");
        }
        throw new Error(data.error || "Failed to get response");
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.reply || data.response || data.message || data.answer || "I'm not sure how to respond to that.",
        sender: "ai",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error. Please try again.",
        sender: "ai",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <>
      <DashNavbar />
      <MagicCard>
        <div className="min-h-screen bg-background dark:bg-black pt-20 pb-4 px-4">
          <div className="max-w-5xl mx-auto h-[calc(100vh-7rem)] flex flex-col">
            {/* Header */}
            <div className="bg-card dark:bg-[#171717] rounded-t-2xl p-6 border-b border-border dark:border-gray-800">
              <h1 className="text-2xl md:text-3xl font-bold text-foreground dark:text-white">
                Legal AI Assistant
              </h1>
              <p className="text-muted-foreground dark:text-gray-400 text-sm mt-1">
                Ask me anything about Indian law, IPC sections, or legal procedures
              </p>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 bg-card dark:bg-[#171717] overflow-y-auto p-4 md:p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${message.sender === "user" ? "justify-end" : "justify-start"
                    }`}
                >
                  {message.sender === "ai" && (
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-cyan-600 flex items-center justify-center">
                      <IconRobot size={20} className="text-white" />
                    </div>
                  )}

                  <div
                    className={`max-w-[75%] md:max-w-[65%] rounded-2xl px-4 py-3 ${message.sender === "user"
                      ? "bg-cyan-600 text-white"
                      : "bg-muted dark:bg-gray-800 text-foreground dark:text-gray-100"
                      }`}
                  >
                    {message.attachment && (
                      <div className="mb-2 p-2 rounded bg-black/10 dark:bg-white/10 flex items-center gap-2">
                        {message.attachment.type === "image" ? (
                          <IconPhoto size={16} />
                        ) : (
                          <IconFileText size={16} />
                        )}
                        <span className="text-xs truncate max-w-[150px]">{message.attachment.name}</span>
                      </div>
                    )}
                    <p className="text-sm md:text-base whitespace-pre-wrap break-words">
                      {message.text}
                    </p>
                    <span suppressHydrationWarning className="text-xs opacity-70 mt-1 block">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>

                  {message.sender === "user" && (
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                      <IconUser size={20} className="text-white" />
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-3 justify-start">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-cyan-600 flex items-center justify-center">
                    <IconRobot size={20} className="text-white" />
                  </div>
                  <div className="bg-muted dark:bg-gray-800 rounded-2xl px-4 py-3">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                        style={{ animationDelay: "0.4s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="bg-card dark:bg-[#171717] rounded-b-2xl p-4 border-t border-border dark:border-gray-800">
              {/* File Preview */}
              {selectedFile && (
                <div className="mb-3 flex items-center gap-2 bg-muted dark:bg-gray-800 p-2 rounded-lg w-fit">
                  <div className="bg-cyan-100 dark:bg-cyan-900/30 p-1.5 rounded">
                    {selectedFile.type.startsWith("image/") ? (
                      <IconPhoto size={18} className="text-cyan-600 dark:text-cyan-400" />
                    ) : (
                      <IconFileText size={18} className="text-cyan-600 dark:text-cyan-400" />
                    )}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-medium text-foreground dark:text-white truncate max-w-[200px]">
                      {selectedFile.name}
                    </span>
                    <span className="text-[10px] text-muted-foreground dark:text-gray-400">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                  <button
                    onClick={clearFile}
                    className="ml-2 p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full transition-colors"
                  >
                    <IconX size={14} className="text-gray-500" />
                  </button>
                </div>
              )}

              <form onSubmit={handleSubmit} className="flex gap-3 items-end">
                {/* File Input (Hidden) */}
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileSelect}
                  className="hidden"
                  accept=".pdf,image/*"
                />

                {/* Attach Button */}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-3 bg-muted dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 
                           text-gray-600 dark:text-gray-300 rounded-xl transition-colors"
                  title="Attach file"
                >
                  <IconPaperclip size={20} />
                </button>

                {/* Mic Button (Disabled) */}
                <button
                  type="button"
                  disabled
                  className="p-3 bg-muted dark:bg-gray-800 text-gray-400 dark:text-gray-600 
                           rounded-xl cursor-not-allowed opacity-70"
                  title="Voice input coming soon"
                >
                  <IconMicrophone size={20} />
                </button>

                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about IPC sections, legal procedures..."
                  disabled={loading}
                  rows={1}
                  className="flex-1 bg-muted dark:bg-gray-800 text-foreground dark:text-white rounded-xl px-4 py-3 
                         border-2 border-yellow-400/40 dark:border-gray-700
                         focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500
                         hover:border-yellow-500/60 dark:hover:border-gray-600
                         resize-none disabled:opacity-50 disabled:cursor-not-allowed
                         placeholder-muted-foreground dark:placeholder-gray-500 text-sm md:text-base
                         transition-all duration-200"
                  style={{ minHeight: "48px", maxHeight: "120px" }}
                />
                <button
                  type="submit"
                  disabled={(!input.trim() && !selectedFile) || loading}
                  aria-label="Send message"
                  title="Send message"
                  className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-700 
                         disabled:cursor-not-allowed text-white rounded-xl px-6 py-3
                         transition-colors flex items-center justify-center
                         flex-shrink-0 h-[48px]"
                >
                  <IconSend size={20} />
                  <span className="sr-only">Send message</span>
                </button>
              </form>
              <p className="text-xs text-muted-foreground dark:text-gray-500 mt-2 text-center">
                Press Enter to send, Shift+Enter for new line
              </p>
            </div>
          </div>
        </div>
      </MagicCard>
      <FooterComponent />
    </>
  );
};

export default ChatbotPage;