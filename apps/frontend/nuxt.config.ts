export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    devtools: { enabled: true },
    modules: [
      ["@prisma/nuxt", { autoSetupPrisma: true }],
      "@nuxtjs/tailwindcss",
      ["shadcn-nuxt", { prefix: "", componentDir: "./components/ui" }],
      ["@nuxtjs/color-mode", { classSuffix: "" }],
      "nuxt-graphql-client",
      "nuxt-auth-utils",
      ["@pinia/nuxt", { storesDirs: ["./stores/**"] }],
      "@nuxt/eslint",
      "@nuxt/icon",
      "@vee-validate/nuxt",
      "@nuxt/image",
    ],
    experimental: {
        typedPages: true,
    },
    alias: {
        pinia: "pinia/dist/pinia.mjs",
    },
});