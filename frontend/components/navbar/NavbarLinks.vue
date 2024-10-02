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
        <NuxtLink class="hidden sm:flex items-center" to="/">
            <Icon
                name="material-symbols-light:home-rounded"
                class="text-xl font-medium text-gray-950"
            />
        </NuxtLink>

        <NuxtLink
            v-for="item in items"
            :key="item.label"
            :to="item.to"
            class="hidden sm:flex"
        >
            {{ capitalize(item.label) }}
        </NuxtLink>

        <DropdownMenu>
            <DropdownMenuTrigger class="sm:hidden">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="30"
                    height="30"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="w-8 h-8"
                >
                    <rect width="7" height="7" x="3" y="3" rx="1" />
                    <rect width="7" height="7" x="14" y="3" rx="1" />
                    <rect width="7" height="7" x="14" y="14" rx="1" />
                    <rect width="7" height="7" x="3" y="14" rx="1" />
                </svg>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
                <DropdownMenuItem>
                    <NuxtLink to="/"> Home </NuxtLink>
                </DropdownMenuItem>
                <DropdownMenuItem v-for="item in items" :key="item.label">
                    <NuxtLink :to="item.to" class="w-full h-full">
                        {{ capitalize(item.label) }}
                    </NuxtLink>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    </nav>
</template>
