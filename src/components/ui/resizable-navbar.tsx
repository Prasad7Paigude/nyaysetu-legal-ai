
"use client";
import { cn } from "@/lib/utils";
import { IconMenu2, IconX } from "@tabler/icons-react";
import {
  motion,
  AnimatePresence,
  useScroll,
  useMotionValueEvent,
} from "motion/react";

import React, { useRef, useState, useEffect } from "react";

interface NavbarProps {
  children: React.ReactNode;
  className?: string;
}

interface NavBodyProps {
  children: React.ReactNode;
  className?: string;
  visible?: boolean;
  isScrolled?: boolean;
}

interface NavItem {
  name: string;
  link?: string;
  submenu?: {
    name: string;
    link: string;
  }[];
}

interface NavItemsProps {
  items: NavItem[];
  className?: string;
  onItemClick?: () => void;
  isScrolled?: boolean;
}

interface MobileNavProps {
  children: React.ReactNode;
  className?: string;
  visible?: boolean;
  isScrolled?: boolean;
}

interface MobileNavHeaderProps {
  children: React.ReactNode;
  className?: string;
}

interface MobileNavMenuProps {
  children: React.ReactNode;
  className?: string;
  isOpen: boolean;
  onClose: () => void;
}

interface MobileNavToggleProps {
  isOpen: boolean;
  onClick: () => void;
  isScrolled?: boolean;
}

interface NavbarLogoProps {
  isScrolled?: boolean;
}

export const Navbar = ({ children, className }: NavbarProps) => {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollY } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });
  const [visible, setVisible] = useState<boolean>(false);

  useMotionValueEvent(scrollY, "change", (latest) => {
    setVisible(latest > 100);
  });

  return (
    <motion.div
      ref={ref}
      className={cn("sticky inset-x-0 top-20 z-40 w-full", className)}
    >
      {React.Children.map(children, (child) =>
        React.isValidElement(child)
          ? React.cloneElement(
            child as React.ReactElement<{ visible?: boolean }>,
            { visible },
          )
          : child,
      )}
    </motion.div>
  );
};

export const NavBody = ({ children, className, visible, isScrolled }: NavBodyProps) => {
  return (
    <motion.div
      animate={{
        width: visible ? "40%" : "100%",
        y: visible ? 20 : 0,
      }}
      transition={{
        type: "spring",
        stiffness: 200,
        damping: 50,
      }}
      style={{ minWidth: "800px" }}
      className={cn(
        "relative z-[60] mx-auto hidden w-full max-w-7xl flex-row items-center justify-between self-start rounded-full px-4 py-2 lg:flex transition-all duration-300",
        visible
          ? "bg-background/70 backdrop-blur-xl border border-border/50 shadow-[0_8px_32px_0_rgba(31,38,135,0.15)]"
          : "bg-transparent dark:bg-transparent backdrop-blur-md border border-transparent",
        className,
      )}
    >
      {children}
    </motion.div>
  );
};

export const NavItems = ({ items, className, onItemClick, isScrolled }: NavItemsProps) => {
  const [hovered, setHovered] = useState<number | null>(null);
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <motion.div
      onMouseLeave={() => setHovered(null)}
      className={cn(
        "hidden flex-1 flex-row items-center justify-center space-x-2 text-sm font-medium transition duration-200 lg:flex lg:space-x-2",
        "text-foreground hover:text-muted-foreground",
        className,
      )}
    >
      {items.map((item, idx) => {
        const hasSubmenu = item.submenu && item.submenu.length > 0;

        return (
          <div
            key={idx}
            className="relative"
            onMouseEnter={() => setHovered(idx)}
            onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
          >
            <a
              onClick={onItemClick}
              className={cn(
                "relative px-4 py-2 cursor-pointer",
                "text-foreground hover:text-muted-foreground"
              )}
              href={item.link || "#"}
            >
              {hovered === idx && !hasSubmenu && (
                <motion.div
                  layoutId="hovered"
                  className={cn(
                    "absolute inset-0 h-full w-full rounded-full",
                    isScrolled ? "bg-muted/50" : "bg-muted/30"
                  )}
                />
              )}
              <span className="relative z-20">{item.name}</span>
            </a>

            {/* Submenu with glass effect */}
            {hasSubmenu && (hovered === idx || openIndex === idx) && (
              <motion.div
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                className="absolute top-full left-0 mt-2 w-40 rounded-xl bg-background/80 backdrop-blur-xl text-foreground shadow-[0_8px_32px_0_rgba(31,38,135,0.2)] z-50 border border-border/50 overflow-hidden"
              >
                {item.submenu?.map((subItem, subIdx) => (
                  <a
                    key={subIdx}
                    href={subItem.link}
                    className="block px-4 py-2 hover:bg-muted/50 transition-colors"
                    onClick={onItemClick}
                  >
                    {subItem.name}
                  </a>
                ))}
              </motion.div>
            )}
          </div>
        );
      })}
    </motion.div>
  );
};

// --- MOBILE NAV COMPONENTS ---
export const MobileNav = ({ children, className, visible, isScrolled }: MobileNavProps) => {
  return (
    <motion.div
      animate={{
        width: visible ? "90%" : "100%",
        paddingRight: visible ? "12px" : "0px",
        paddingLeft: visible ? "12px" : "0px",
        borderRadius: visible ? "4px" : "2rem",
        y: visible ? 20 : 0,
      }}
      transition={{ type: "spring", stiffness: 200, damping: 50 }}
      className={cn(
        "relative z-50 mx-auto flex w-full max-w-[calc(100vw-2rem)] flex-col items-center justify-between px-0 py-2 lg:hidden transition-all duration-300",
        visible
          ? "bg-background/70 backdrop-blur-xl border border-border/50 shadow-[0_8px_32px_0_rgba(31,38,135,0.15)]"
          : "bg-transparent dark:bg-transparent backdrop-blur-md border border-transparent",
        className,
      )}
    >
      {children}
    </motion.div>
  );
};

export const MobileNavHeader = ({
  children,
  className,
}: MobileNavHeaderProps) => (
  <div className={cn("flex w-full flex-row items-center justify-between", className)}>
    {children}
  </div>
);

export const MobileNavMenu = ({
  children,
  className,
  isOpen,
  onClose,
}: MobileNavMenuProps) => (
  <AnimatePresence>
    {isOpen && (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className={cn(
          "absolute inset-x-0 top-16 z-50 flex w-full flex-col items-start justify-start gap-4 rounded-lg bg-background/90 backdrop-blur-xl px-4 py-8 shadow-[0_8px_32px_0_rgba(31,38,135,0.2)] border border-border/50",
          className,
        )}
      >
        {children}
      </motion.div>
    )}
  </AnimatePresence>
);

export const MobileNavToggle = ({
  isOpen,
  onClick,
  isScrolled,
}: MobileNavToggleProps) => (isOpen ? (
  <IconX
    className={cn(
      "transition-colors cursor-pointer",
      "text-foreground"
    )}
    onClick={onClick}
  />
) : (
  <IconMenu2
    className={cn(
      "transition-colors cursor-pointer",
      "text-foreground"
    )}
    onClick={onClick}
  />
));

export const NavbarLogo = ({ isScrolled }: NavbarLogoProps) => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const updateTheme = () => {
      setIsDark(document.documentElement.classList.contains("dark"));
    };

    updateTheme();

    const observer = new MutationObserver(updateTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });

    return () => observer.disconnect();
  }, []);

  // When scrolled: use theme-based logo (logo.png for light, logo2.png for dark)
  // When not scrolled: always use logo2.png (white logo on black background)
  // When scrolled: use theme-based logo (logo.png for light, logo2.png for dark)
  // When not scrolled: always use logo2.png (white logo on black background)
  const logoSrc = isDark ? "/logo2.png" : "/logo.png";

  return (
    <a
      href="#"
      className="relative z-20 mr-4 flex items-center space-x-2 px-2 py-1 text-xl font-bold"
    >
      <img src={logoSrc} alt="logo" width={50} height={50} />
      <span className={cn(
        "font-bold transition-colors",
        "text-foreground"
      )}>
        NyaySetu AI
      </span>
    </a>
  );
};

export const NavbarButton = ({
  href,
  as: Tag = "a",
  children,
  className,
  variant = "primary",
  ...props
}: {
  href?: string;
  as?: React.ElementType;
  children: React.ReactNode;
  className?: string;
  variant?: "primary" | "secondary" | "dark" | "gradient";
} & (React.ComponentPropsWithoutRef<"a"> | React.ComponentPropsWithoutRef<"button">)) => {
  const baseStyles =
    "px-4 py-2 rounded-md bg-white button bg-white text-black text-sm font-bold relative cursor-pointer hover:-translate-y-0.5 transition duration-200 inline-block text-center";

  const variantStyles = {
    primary:
      "shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset]",
    secondary: "bg-transparent shadow-none dark:text-white",
    dark: "bg-black text-white shadow-[0_0_24px_rgba(34,_42,_53,_0.06),_0_1px_1px_rgba(0,_0,_0,_0.05),_0_0_0_1px_rgba(34,_42,_53,_0.04),_0_0_4px_rgba(34,_42,_53,_0.08),_0_16px_68px_rgba(47,_48,_55,_0.05),_0_1px_0_rgba(255,_255,_255,_0.1)_inset]",
    gradient: "bg-gradient-to-b from-blue-500 to-blue-700 text-white shadow-[0px_2px_0px_0px_rgba(255,255,255,0.3)_inset]",
  };

  return (
    <Tag href={href || undefined} className={cn(baseStyles, variantStyles[variant], className)} {...props}>
      {children}
    </Tag>
  );
};