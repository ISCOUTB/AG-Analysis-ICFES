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
        "@formkit/auto-animate",
        [
            "nuxt-openapi-docs-module",
            {
                folder: "./docs/openapi",
                name: "API Docs",
                files: function () {
                    return {
                        page: "API Documentation",
                    };
                },
                debugger: true,
                list: true,
                locales: ["en", "fr", "es"],
            },
        ],
    ],
    experimental: {
        typedPages: true,
    },
    alias: {
        pinia: "pinia/dist/pinia.mjs",
    },
    imports: {
        dirs: ["composables/**"],
    },
});
