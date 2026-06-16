"use client";

import React, { useState } from "react";
import DashNavbar from "@/components/navbar/DashNavbar";
import FooterComponent from "@/components/footer/FooterComponent";
import { platformDocs } from "@/lib/platform-docs";
import { IconChevronRight, IconChevronDown, IconBook } from "@tabler/icons-react";

export default function PlatformGuidePage() {
    const [activeSection, setActiveSection] = useState("what-is-nyaysetuai");
    const [expandedSections, setExpandedSections] = useState<string[]>(["introduction"]);

    const toggleSection = (sectionId: string) => {
        if (expandedSections.includes(sectionId)) {
            setExpandedSections(expandedSections.filter((id) => id !== sectionId));
        } else {
            setExpandedSections([...expandedSections, sectionId]);
        }
    };

    const activePage = platformDocs
        .flatMap((section) => section.pages)
        .find((page) => page.id === activeSection);

    return (
        <>
            <DashNavbar />
            <div className="min-h-screen bg-background dark:bg-black pt-20">
                <div className="max-w-[1600px] mx-auto px-4">
                    {/* Header */}
                    <div className="py-8 border-b border-gray-200 dark:border-gray-800">
                        <div className="flex items-center gap-3 mb-2">
                            <IconBook className="w-8 h-8 text-cyan-600 dark:text-cyan-400" />
                            <h1 className="text-4xl font-bold text-foreground dark:text-white">
                                NyaySetuAI Platform Guide
                            </h1>
                        </div>
                        <p className="text-muted-foreground dark:text-gray-400 text-lg">
                            Complete documentation for understanding and using the NyaySetuAI Legal Assistance Platform
                        </p>
                    </div>

                    {/* Two-Panel Layout */}
                    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-8 py-8">
                        {/* LEFT SIDEBAR - Navigation */}
                        <aside className="lg:sticky lg:top-24 lg:h-[calc(100vh-8rem)] lg:overflow-y-auto">
                            <nav className="space-y-1 bg-card dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-800">
                                {platformDocs.map((section) => (
                                    <div key={section.id} className="mb-2">
                                        <button
                                            onClick={() => toggleSection(section.id)}
                                            className="flex items-center justify-between w-full text-left px-3 py-2 rounded-md font-semibold text-foreground dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                                        >
                                            <span>{section.title}</span>
                                            {expandedSections.includes(section.id) ? (
                                                <IconChevronDown className="w-4 h-4" />
                                            ) : (
                                                <IconChevronRight className="w-4 h-4" />
                                            )}
                                        </button>

                                        {expandedSections.includes(section.id) && (
                                            <div className="ml-2 mt-1 space-y-1 border-l-2 border-gray-200 dark:border-gray-700 pl-2">
                                                {section.pages.map((page) => (
                                                    <button
                                                        key={page.id}
                                                        onClick={() => setActiveSection(page.id)}
                                                        className={`block w-full text-left px-3 py-2 text-sm rounded-md transition-colors ${activeSection === page.id
                                                            ? "bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300 font-medium"
                                                            : "text-muted-foreground dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                                                            }`}
                                                    >
                                                        {page.title}
                                                    </button>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </nav>
                        </aside>

                        {/* RIGHT PANEL - Content */}
                        <main className="bg-card dark:bg-gray-900 rounded-lg p-8 border border-gray-200 dark:border-gray-800 min-h-[600px]">
                            {activePage && (
                                <article className="prose prose-lg dark:prose-invert max-w-none">
                                    <style jsx>{`
                                        article :global(h2) {
                                            font-size: 1.875rem;
                                            font-weight: 700;
                                            margin-top: 2.5rem;
                                            margin-bottom: 1rem;
                                            border-bottom: 1px solid rgba(229, 231, 235, 0.2);
                                            padding-bottom: 0.5rem;
                                        }
                                        
                                        article :global(h3) {
                                            font-size: 1.5rem;
                                            font-weight: 600;
                                            margin-top: 2rem;
                                            margin-bottom: 0.75rem;
                                        }
                                        
                                        article :global(h4) {
                                            font-size: 1.25rem;
                                            font-weight: 600;
                                            margin-top: 1.5rem;
                                            margin-bottom: 0.5rem;
                                        }
                                        
                                        article :global(p) {
                                            line-height: 1.75;
                                            margin-bottom: 1.5rem;
                                            color: inherit;
                                        }
                                        
                                        article :global(ul),
                                        article :global(ol) {
                                            margin: 1.5rem 0;
                                            padding-left: 1.5rem;
                                            line-height: 1.75;
                                        }
                                        
                                        article :global(li) {
                                            margin-bottom: 0.75rem;
                                        }
                                        
                                        article :global(code) {
                                            background: rgba(110, 118, 129, 0.15);
                                            padding: 0.2em 0.4em;
                                            border-radius: 6px;
                                            font-size: 0.875em;
                                            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                                            font-weight: 400;
                                        }
                                        
                                        article :global(a) {
                                            color: #3b82f6;
                                            text-decoration: none;
                                            font-weight: 500;
                                        }
                                        
                                        article :global(a:hover) {
                                            text-decoration: underline;
                                        }
                                        
                                        article :global(strong) {
                                            font-weight: 600;
                                        }
                                        
                                        article :global(table) {
                                            width: 100%;
                                            margin: 1.5rem 0;
                                            border-collapse: collapse;
                                        }
                                        
                                        article :global(th),
                                        article :global(td) {
                                            padding: 0.75rem 1rem;
                                            text-align: left;
                                            border-bottom: 1px solid rgba(229, 231, 235, 0.2);
                                        }
                                        
                                        article :global(th) {
                                            font-weight: 600;
                                            background: rgba(59, 130, 246, 0.05);
                                        }
                                        
                                        article :global(blockquote) {
                                            border-left: 3px solid #3b82f6;
                                            padding-left: 1rem;
                                            margin: 1.5rem 0;
                                            font-style: italic;
                                            color: rgba(107, 114, 128, 1);
                                        }
                                        
                                        article :global(div[style*="background: rgba(59, 130, 246"]) {
                                            background: rgba(59, 130, 246, 0.1) !important;
                                            border-left: 3px solid #3b82f6 !important;
                                            padding: 1rem !important;
                                            border-radius: 0.5rem !important;
                                            margin: 1.5rem 0 !important;
                                        }
                                    `}</style>
                                    <div dangerouslySetInnerHTML={{ __html: activePage.content }} />
                                </article>
                            )}
                        </main>
                    </div>
                </div>
            </div>
            <FooterComponent />
        </>
    );
}
