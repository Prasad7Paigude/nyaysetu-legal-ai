
"use client";
import Link from "next/link";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import {
  IconBrandTwitter,
  IconBrandLinkedin,
  IconBrandGithub,
  IconBrandInstagram,
  IconMail,
  IconPhone,
  IconMapPin
} from "@tabler/icons-react";

export default function FooterComponent() {
  const { resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const navItems = [
    { name: "Home", link: "/" },
    { name: "AI Chatbot", link: "/chatbot" },
    { name: "Advantages", link: "/advantages" },
    { name: "Training", link: "/training" },
  ];

  const legalItems = [
    { name: "Privacy Policy", link: "/privacy" },
    { name: "Terms of Service", link: "/terms" },
    { name: "Cookie Policy", link: "/cookies" },
  ];

  const socialLinks = [
    { icon: IconBrandTwitter, href: "#", label: "Twitter" },
    { icon: IconBrandLinkedin, href: "#", label: "LinkedIn" },
    { icon: IconBrandGithub, href: "#", label: "GitHub" },
    { icon: IconBrandInstagram, href: "#", label: "Instagram" },
  ];

  // Prevent hydration mismatch by rendering a placeholder or default until mounted
  const logoSrc = mounted && resolvedTheme === "dark" ? "/logo2.png" : "/logo.png";

  return (
    <footer className="bg-background text-foreground border-t-2 border-accent transition-colors">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Section */}
          <div className="flex flex-col gap-4">
            <Link href="/" className="flex items-center gap-2">
              <img src={logoSrc} alt="NyaySetu AI Logo" width={40} height={40} className="object-contain" />
              <span className="text-xl font-bold">NyaySetu AI</span>
            </Link>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed max-w-xs">
              Empowering legal professionals and citizens with AI-driven solutions for smarter, faster, and more accessible justice.
            </p>
            <div className="flex gap-4 mt-2">
              {socialLinks.map((social, idx) => (
                <a
                  key={idx}
                  href={social.href}
                  aria-label={social.label}
                  className="text-gray-500 hover:text-cyan-600 dark:text-gray-400 dark:hover:text-cyan-400 transition-colors"
                >
                  <social.icon size={20} />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-semibold">Quick Links</h3>
            <ul className="flex flex-col gap-2">
              {navItems.map((item, idx) => (
                <li key={idx}>
                  <Link
                    href={item.link}
                    className="text-gray-600 dark:text-gray-400 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors text-sm"
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-semibold">Legal</h3>
            <ul className="flex flex-col gap-2">
              {legalItems.map((item, idx) => (
                <li key={idx}>
                  <Link
                    href={item.link}
                    className="text-gray-600 dark:text-gray-400 hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors text-sm"
                  >
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-semibold">Contact Us</h3>
            <ul className="flex flex-col gap-3">
              <li className="flex items-start gap-3 text-sm text-gray-600 dark:text-gray-400">
                <IconMail size={18} className="mt-0.5 shrink-0" />
                <a href="mailto:support@nyaysetu.ai" className="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors">
                  support@nyaysetu.ai
                </a>
              </li>
              <li className="flex items-start gap-3 text-sm text-gray-600 dark:text-gray-400">
                <IconPhone size={18} className="mt-0.5 shrink-0" />
                <a href="tel:+911234567890" className="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors">
                  +91 932*****10
                </a>
              </li>
              <li className="flex items-start gap-3 text-sm text-gray-600 dark:text-gray-400">
                <IconMapPin size={18} className="mt-0.5 shrink-0" />
                <span>
                  Legal Tech Hub,<br />
                  Hinjewadi Phase 1,<br />
                  Pune, Maharashtra 411057
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-200 dark:border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-gray-500 dark:text-gray-500 text-sm text-center md:text-left">
            &copy; {new Date().getFullYear()} NyaySetu AI. All rights reserved.
          </p>
          <div className="flex gap-6 text-sm text-gray-500 dark:text-gray-500">
            <Link href="/privacy" className="hover:text-gray-900 dark:hover:text-white transition-colors">Privacy</Link>
            <Link href="/terms" className="hover:text-gray-900 dark:hover:text-white transition-colors">Terms</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

