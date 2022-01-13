module.exports = {
  darkMode: false, // or 'media' or 'class'
  theme: {
    backdropFilter: {
      none: "none",
      blur: "blur(20px)",
    },
  },
  variants: {
    opacity: ({ after }) => after(["disabled"]),
    scrollbar: ["rounded"],
  },
  purge: {
    enabled: true,
    content: ["./**/*.html"],
  },
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === "production" ? { cssnano: {} } : {}),
  },
};
