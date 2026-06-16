"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface ShinyButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    children: React.ReactNode;
    className?: string;
}

export const ShinyButton = ({ children, className, ...props }: ShinyButtonProps) => {
    return (
        <button
            className={cn(
                "group/btn relative h-10 w-full rounded-md bg-primary text-primary-foreground font-medium shadow-[0px_1px_0px_0px_#00000040_inset,0px_-1px_0px_0px_#00000040_inset] transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center",
                className
            )}
            {...props}
        >
            {children}
            <BottomGradient />
        </button>
    );
};

const BottomGradient = () => {
    return (
        <>
            <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition-opacity duration-500 group-hover/btn:opacity-100" />
            <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition-opacity duration-500 group-hover/btn:opacity-100" />
        </>
    );
};
