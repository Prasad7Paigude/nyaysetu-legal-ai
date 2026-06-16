"use client"

import { useCallback, useRef, useState, useEffect } from "react"
import { Moon, Sun } from "lucide-react"
import { flushSync } from "react-dom"
import { useTheme } from "next-themes"

import { cn } from "@/lib/utils"

interface AnimatedThemeTogglerProps
  extends React.ComponentPropsWithoutRef<"button"> {
  duration?: number
}

export const AnimatedThemeToggler = ({
  className,
  duration = 400,
  ...props
}: AnimatedThemeTogglerProps) => {
  const { theme, setTheme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const buttonRef = useRef<HTMLButtonElement>(null)
  const isTogglingRef = useRef(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const toggleTheme = useCallback((e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    e.stopPropagation()

    if (isTogglingRef.current) return
    isTogglingRef.current = true

    const isDark = resolvedTheme === "dark"
    const newTheme = isDark ? "light" : "dark"

    // Check if View Transition API is supported
    if (!document.startViewTransition || !buttonRef.current) {
      setTheme(newTheme)
      setTimeout(() => {
        isTogglingRef.current = false
      }, 100)
      return
    }

    const { top, left, width, height } = buttonRef.current.getBoundingClientRect()
    const x = left + width / 2
    const y = top + height / 2
    const maxRadius = Math.hypot(
      Math.max(left, window.innerWidth - left),
      Math.max(top, window.innerHeight - top)
    )

    const transition = document.startViewTransition(() => {
      flushSync(() => {
        setTheme(newTheme)
      })
    })

    transition.ready.then(() => {
      document.documentElement.animate(
        {
          clipPath: [
            `circle(0px at ${x}px ${y}px)`,
            `circle(${maxRadius}px at ${x}px ${y}px)`,
          ],
        },
        {
          duration,
          easing: "ease-in-out",
          pseudoElement: "::view-transition-new(root)",
        }
      )
    })

    transition.finished.finally(() => {
      isTogglingRef.current = false
    })
  }, [resolvedTheme, setTheme, duration])

  // Prevent hydration mismatch
  if (!mounted) {
    return (
      <button
        className={cn(className)}
        aria-label="Toggle theme"
        {...props}
      >
        <div className="h-5 w-5" />
      </button>
    )
  }

  const isDark = resolvedTheme === "dark"

  return (
    <button
      ref={buttonRef}
      onClick={toggleTheme}
      type="button"
      className={cn(className)}
      aria-label="Toggle theme"
      {...props}
    >
      {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      <span className="sr-only">Toggle theme</span>
    </button>
  )
}
