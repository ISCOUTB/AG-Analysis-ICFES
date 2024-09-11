<script setup lang="ts">
    import { capitalize } from "vue";

    const items: NavbarLinkItem[] = [
        {
            label: "features",
            to: "/features",
        },
        {
            label: "pricing",
            to: "/",
        },
        {
            label: "about",
            to: "/about",
        },
        {
            label: "contact",
            to: "/",
        },
    ];
</script>

<template>
    <nav class="flex items-center gap-4 sm:gap-6">
        <NuxtLink v-for="item in items" :key="item.label" :to="item.to">
            {{ capitalize(item.label) }}
        </NuxtLink>
    </nav>
</template>
