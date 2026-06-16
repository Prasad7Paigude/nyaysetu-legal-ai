"use client";
import { useState, useEffect } from "react";
import {
  Navbar,
  NavBody,
  NavItems,
  MobileNav,
  MobileNavToggle,
  MobileNavHeader,
  MobileNavMenu,
  NavbarLogo,
} from "@/components/ui/resizable-navbar";
import { ShimmerButton } from "@/components/ui/shimmer-button";
import Link from "next/link";
import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler";

export default function NavbarComponent() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileSubmenuOpen, setMobileSubmenuOpen] = useState<number | null>(null);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 100);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navItems = [
    { name: "Home", link: "/" },
    { name: "AI Chatbot", link: "/login" },
    {
      name: "More",
      submenu: [
        { name: "Your Uploads", link: "/login" },
        { name: "Predict IPC", link: "/ipcpredication" },
        { name: "Generate Draft", link: "/generatedraft" },
        { name: "Newsletter", link: "/newsletter" },
        { name: "Platform Guide", link: "/platformguide" },
        { name: "About", link: "/about" },
      ],
    },
  ];

  return (
    <Navbar className="fixed top-0 left-0 w-full z-50">
      {/* 🖥️ Desktop Navbar */}
      <NavBody isScrolled={isScrolled}>
        <NavbarLogo isScrolled={isScrolled} />
        <NavItems items={navItems} isScrolled={isScrolled} />

        <div className="flex items-center gap-4">
          <AnimatedThemeToggler
            className="relative z-50 cursor-pointer text-2xl p-1 rounded-full transition-colors text-foreground hover:text-muted-foreground"
          />
          <Link href="/login">
            <ShimmerButton
              background="var(--primary)"
              shimmerColor="var(--primary-foreground)"
              className="text-primary-foreground dark:[--bg:var(--accent)] dark:[--shimmer-color:var(--accent-foreground)] dark:text-accent-foreground"
            >
              Log In
            </ShimmerButton>
          </Link>

          <Link href="/signup">
            <ShimmerButton
              background="var(--primary)"
              shimmerColor="var(--primary-foreground)"
              className="text-primary-foreground dark:[--bg:var(--accent)] dark:[--shimmer-color:var(--accent-foreground)] dark:text-accent-foreground"
            >
              Sign Up
            </ShimmerButton>
          </Link>
        </div>
      </NavBody>

      {/* 📱 Mobile Navbar */}
      <MobileNav isScrolled={isScrolled}>
        <MobileNavHeader>
          <NavbarLogo isScrolled={isScrolled} />
          <div className="flex items-center gap-2">
            <AnimatedThemeToggler
              className="text-xl p-1 transition-colors text-foreground"
            />
            <MobileNavToggle
              isOpen={menuOpen}
              isScrolled={isScrolled}
              onClick={() => setMenuOpen(!menuOpen)}
            />
          </div>
        </MobileNavHeader>

        <MobileNavMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)}>
          {navItems.map((item, index) => (
            <div key={index} className="w-full">
              {item.submenu ? (
                <div>
                  <button
                    onClick={() =>
                      setMobileSubmenuOpen(mobileSubmenuOpen === index ? null : index)
                    }
                    className="flex w-full items-center justify-between text-lg font-medium text-foreground py-2"
                  >
                    {item.name}
                    <span className={`transform transition-transform ${mobileSubmenuOpen === index ? "rotate-180" : ""}`}>
                      ▼
                    </span>
                  </button>
                  {mobileSubmenuOpen === index && (
                    <div className="ml-4 flex flex-col gap-2 border-l border-border pl-4">
                      {item.submenu.map((subItem, subIndex) => (
                        <a
                          key={subIndex}
                          href={subItem.link}
                          className="text-base text-muted-foreground hover:text-foreground py-1"
                          onClick={() => setMenuOpen(false)}
                        >
                          {subItem.name}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <a
                  href={item.link}
                  className="block text-lg font-medium text-foreground py-2"
                  onClick={() => setMenuOpen(false)}
                >
                  {item.name}
                </a>
              )}
            </div>
          ))}

          {/* Login/Signup Buttons for Mobile */}
          <div className="mt-4 flex w-full flex-col gap-4 border-t border-border pt-4">
            <Link href="/login" className="w-full" onClick={() => setMenuOpen(false)}>
              <ShimmerButton
                background="var(--primary)"
                shimmerColor="var(--primary-foreground)"
                className="w-full justify-center text-primary-foreground dark:[--bg:var(--accent)] dark:[--shimmer-color:var(--accent-foreground)] dark:text-accent-foreground"
              >
                Log In
              </ShimmerButton>
            </Link>

            <Link href="/signup" className="w-full" onClick={() => setMenuOpen(false)}>
              <ShimmerButton
                background="var(--primary)"
                shimmerColor="var(--primary-foreground)"
                className="w-full justify-center text-primary-foreground dark:[--bg:var(--accent)] dark:[--shimmer-color:var(--accent-foreground)] dark:text-accent-foreground"
              >
                Sign Up
              </ShimmerButton>
            </Link>
          </div>
        </MobileNavMenu>
      </MobileNav>
    </Navbar>
  );
}
