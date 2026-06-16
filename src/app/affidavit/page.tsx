'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useTheme } from 'next-themes';
import { useSession } from '@/lib/auth-client';
import NavbarComponent from '@/components/navbar/NavbarComponent';
import DashNavbar from '@/components/navbar/DashNavbar';
import FooterComponent from '@/components/footer/FooterComponent';
import { MagicCard } from '@/components/ui/magic-card';

interface AffidavitData {
    name: string;
    father_name: string;
    mother_name: string;
    spouse_name: string;
    dob: string;
    address: string;
    residence_from: string;
    place: string;
    date: string;
}

export default function AffidavitGeneratorPage() {
    const [formData, setFormData] = useState<AffidavitData>({
        name: '',
        father_name: '',
        mother_name: '',
        spouse_name: '',
        dob: '',
        address: '',
        residence_from: '',
        place: '',
        date: new Date().toLocaleDateString('en-IN'),
    });

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [mounted, setMounted] = useState(false);

    const { resolvedTheme } = useTheme();
    const { data: session } = useSession();

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        try {
            const response = await fetch('/api/generate-affidavit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Failed to generate PDF' }));
                throw new Error(errorData.error || 'Failed to generate PDF');
            }

            // Get the PDF blob
            const blob = await response.blob();

            // Create a download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `NyaySetu_Affidavit_${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show success message
            setSuccessMessage('🎉 Affidavit generated successfully! Check your downloads.');

            // Reset form after 3 seconds
            setTimeout(() => {
                setSuccessMessage(null);
            }, 5000);

        } catch (err) {
            console.error('Error:', err);
            setError(err instanceof Error ? err.message : 'An unexpected error occurred');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
            {session ? <DashNavbar /> : <NavbarComponent />}

            {/* Hero Section */}
            <section className="relative pt-32 pb-12 px-4 md:px-8 flex flex-col items-center text-center overflow-hidden">
                {/* Background Gradient */}
                <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary/10 via-background to-background opacity-50" />

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="max-w-4xl mx-auto mb-8"
                >
                    <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/70 mb-4 pb-2 leading-tight">
                        Affidavit Generator
                    </h1>
                    <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
                        Generate professional affidavit documents instantly. Fill in your details and download a formatted PDF.
                    </p>
                </motion.div>
            </section>

            {/* Form Section */}
            <section className="py-8 px-4 md:px-8 max-w-5xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                >
                    {/* Success Message */}
                    {successMessage && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-6 py-4 rounded-lg mb-6 shadow-md"
                        >
                            <p className="font-medium text-center">{successMessage}</p>
                        </motion.div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 px-6 py-4 rounded-lg mb-6 shadow-md"
                        >
                            <p className="font-medium">Error</p>
                            <p className="text-sm">{error}</p>
                        </motion.div>
                    )}

                    <MagicCard
                        className="p-8 md:p-10 rounded-xl"
                        gradientColor={mounted && resolvedTheme === 'dark' ? '#223542' : '#D8E2EB'}
                    >
                        <form onSubmit={handleSubmit} className="space-y-8">
                            {/* Personal Information Section */}
                            <div>
                                <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center gap-2">
                                    <UserIcon />
                                    Personal Information
                                </h2>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Full Name <span className="text-red-500">*</span>
                                        </label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleInputChange}
                                            required
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                            placeholder="Enter your full name"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Father's Name <span className="text-red-500">*</span>
                                        </label>
                                        <input
                                            type="text"
                                            name="father_name"
                                            value={formData.father_name}
                                            onChange={handleInputChange}
                                            required
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                            placeholder="Enter father's name"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Mother's Name <span className="text-red-500">*</span>
                                        </label>
                                        <input
                                            type="text"
                                            name="mother_name"
                                            value={formData.mother_name}
                                            onChange={handleInputChange}
                                            required
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                            placeholder="Enter mother's name"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Spouse Name <span className="text-muted-foreground text-xs">(Optional)</span>
                                        </label>
                                        <input
                                            type="text"
                                            name="spouse_name"
                                            value={formData.spouse_name}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                            placeholder="Enter spouse name"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Date of Birth <span className="text-muted-foreground text-xs">(DD/MM/YYYY)</span>
                                        </label>
                                        <input
                                            type="text"
                                            name="dob"
                                            value={formData.dob}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                            placeholder="15/08/1990"
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Address Information Section */}
                            <div>
                                <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center gap-2">
                                    <HomeIcon />
                                    Address Details
                                </h2>

                                <div className="grid grid-cols-1 gap-6">
                                    <div>
                                        <label className="block text-sm font-semibold text-foreground mb-2">
                                            Complete Address <span className="text-red-500">*</span>
                                        </label>
                                        <textarea
                                            name="address"
                                            value={formData.address}
                                            onChange={handleInputChange}
                                            required
                                            rows={3}
                                            className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none resize-none"
                                            placeholder="Enter your complete address with city and pincode"
                                        />
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                        <div>
                                            <label className="block text-sm font-semibold text-foreground mb-2">
                                                Resident Since <span className="text-muted-foreground text-xs">(Year)</span>
                                            </label>
                                            <input
                                                type="text"
                                                name="residence_from"
                                                value={formData.residence_from}
                                                onChange={handleInputChange}
                                                className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                                placeholder="2020"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-semibold text-foreground mb-2">
                                                Place <span className="text-muted-foreground text-xs">(City)</span>
                                            </label>
                                            <input
                                                type="text"
                                                name="place"
                                                value={formData.place}
                                                onChange={handleInputChange}
                                                className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                                placeholder="Mumbai"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-semibold text-foreground mb-2">
                                                Date <span className="text-muted-foreground text-xs">(DD/MM/YYYY)</span>
                                            </label>
                                            <input
                                                type="text"
                                                name="date"
                                                value={formData.date}
                                                onChange={handleInputChange}
                                                className="w-full px-4 py-3 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-background text-foreground transition-all outline-none"
                                                placeholder="29/12/2025"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Submit Button */}
                            <div className="pt-4">
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-bold py-4 px-8 rounded-lg transition-all shadow-lg hover:shadow-xl active:scale-95 duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                                >
                                    {isLoading ? (
                                        <span className="flex items-center justify-center gap-3">
                                            <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                                                <circle
                                                    className="opacity-25"
                                                    cx="12"
                                                    cy="12"
                                                    r="10"
                                                    stroke="currentColor"
                                                    strokeWidth="4"
                                                    fill="none"
                                                />
                                                <path
                                                    className="opacity-75"
                                                    fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                                />
                                            </svg>
                                            Generating Your Affidavit...
                                        </span>
                                    ) : (
                                        <span className="flex items-center justify-center gap-2 text-lg">
                                            <DocumentIcon />
                                            Generate Affidavit PDF
                                        </span>
                                    )}
                                </button>
                            </div>

                            {/* Information Note */}
                            <div className="bg-muted/50 border border-border rounded-lg p-6">
                                <div className="flex gap-3">
                                    <InfoIcon />
                                    <div className="flex-1">
                                        <p className="text-sm text-foreground font-semibold mb-2">Important Information</p>
                                        <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                                            <li>Fields marked with <span className="text-red-500 font-semibold">*</span> are mandatory</li>
                                            <li>The PDF will be automatically downloaded to your device</li>
                                            <li>Ensure all information is accurate before generating</li>
                                            <li>Generated documents are for legal purposes</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </MagicCard>
                </motion.div>

                {/* Features Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                    className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
                >
                    <FeatureCard
                        icon={<FastIcon />}
                        title="Instant Generation"
                        description="Generate professionally formatted affidavits in seconds"
                    />
                    <FeatureCard
                        icon={<SecureIcon />}
                        title="Secure & Private"
                        description="Your data is processed securely and not stored"
                    />
                    <FeatureCard
                        icon={<ProfessionalIcon />}
                        title="Professional Format"
                        description="Legally compliant PDF format ready for submission"
                    />
                </motion.div>
            </section>

            <FooterComponent />
        </div>
    );
}

// Feature Card Component
function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
    const { resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    return (
        <MagicCard
            className="p-6 flex flex-col items-center text-center gap-4 hover:scale-105 transition-transform duration-300 shadow-sm hover:shadow-md rounded-lg"
            gradientColor={mounted && resolvedTheme === 'dark' ? '#D9D9D955' : '#D9D9D955'}
        >
            <div className="p-3 rounded-lg bg-primary/10 text-primary dark:text-accent">
                {icon}
            </div>
            <h3 className="text-lg font-bold text-foreground">{title}</h3>
            <p className="text-sm text-muted-foreground">{description}</p>
        </MagicCard>
    );
}

// Icons
const UserIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
    </svg>
);

const HomeIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
);

const DocumentIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
        <polyline points="14 2 14 8 20 8" />
    </svg>
);

const InfoIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary flex-shrink-0 mt-0.5">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 16v-4" />
        <path d="M12 8h.01" />
    </svg>
);

const FastIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
);

const SecureIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
);

const ProfessionalIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <polyline points="10 9 9 9 8 9" />
    </svg>
);
