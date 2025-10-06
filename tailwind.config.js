module.exports = {
    content: ["./templates/**/*.html"],
    safelist: ["bg-green-500", "bg-red-500", "bg-yellow-500", "bg-blue-500"],
    theme: {
        colors: {
            white: "#FFFFFF",
            black: "#000000",
            gray: {
                100: "#F3F4F6",
                200: "#E5E7EB",
                300: "#D1D5DB",
                400: "#9CA3AF",
                500: "#6B7280",
                600: "#4B5563",
                700: "#374151",
                800: "#1F2937",
                900: "#111827",
            },
            orange: {
                500: "#ED7F2B",
                600: "#ED9F2B",
                700: "#ED5B2B",
            },
            yellow: {
                100: "#F5C276",
                500: "#EDB62B",
                700: "#EDD02B",
            },
            green: {
                500: "#22C55E",
                600: "#16A34A",
            },
            red: {
                500: "#EF4444",
            },
        },
    },
    plugins: [],
};
