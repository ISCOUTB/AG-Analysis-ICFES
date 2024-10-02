export default defineNuxtRouteMiddleware(() => {
    if (process.env.NODE_ENV !== "development") {
        return navigateTo("/");
    }
});
