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
        [
            "@pinia/nuxt",
            { storesDirs: ["./stores/**"], alias: "pinia/dist/pinia.mjs" },
        ],
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
    imports: {
        dirs: ["composables/**"],
    },
    runtimeConfig: {
        oauth: {
            github: {
                clientId: process.env.GITHUB_CLIENT_ID,
                clientSecret: process.env.GITHUB_CLIENT_SECRET,
            },
            google: {
                clientId: process.env.GOOGLE_CLIENT_ID,
                clientSecret: process.env.GOOGLE_CLIENT_SECRET,
            },
        },
        sessionPassword: process.env.NUXT_SESSION_PASSWORD,
        databaseURL: process.env.DATABASE_URL,
        public: {
            GQL_HOST: process.env.GQL_HOST,
        },
    },
});
