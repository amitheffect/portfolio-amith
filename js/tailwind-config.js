tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#3b82f6",
                "midnight": "#0a1120",
                "midnight-light": "#131e32",
                "glass-border": "rgba(255, 255, 255, 0.08)",
                "glass-bg": "rgba(255, 255, 255, 0.03)",
            },
            fontFamily: {
                "sans": ["Inter", "sans-serif"],
                "serif": ["Playfair Display", "serif"],
            },
            backgroundImage: {
                'noise': "url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MDAiIGhlaWdodD0iNDAwIj48ZmlsdGVyIGlkPSJnoiPjxmZVR1cmJ1bGVuY2UgdHlwZT0iZnJhY3RhbE5vaXNlIiBiYXNlRnJlcXVlbmN5PSIwLjY1IiBudW1PY3RhdmVzPSIzIiBzdGl0Y2hUaWxlcz0ic3RpdGNoIi8+PC9maWx0ZXI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsdGVyPSJ1cmwoI2cpIiBvcGFjaXR5PSIwLjA1Ii8+PC9zdmc+')",
                'gradient-glow': 'radial-gradient(circle at 50% -20%, rgba(59, 130, 246, 0.15), transparent 70%)',
                'lens-flare': 'radial-gradient(circle at 80% 20%, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 20%), radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.3) 0%, rgba(99, 102, 241, 0) 30%)',
            },
            animation: {
                'spin-slow': 'spin 60s linear infinite',
                'float': 'float 6s ease-in-out infinite',
                'float-delayed': 'float 8s ease-in-out infinite 2s',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                }
            }
        },
    },
}
