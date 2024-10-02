<script setup lang="ts">
    import { capitalize } from "vue";

    const colorMode = useColorMode();
    const colorModeOptions: ColorModeOption[] = [
        {
            label: "system",
            icon: "tdesign:system-code",
            action: () => (colorMode.preference = "system"),
        },
        {
            label: "light",
            icon: "material-symbols:light-mode",
            action: () => (colorMode.preference = "light"),
        },
        {
            label: "dark",
            icon: "mdi:weather-night",
            action: () => (colorMode.preference = "dark"),
        },
    ];

    const icon = computed(() => {
        const selectedMode = colorModeOptions.find(
            (mode) => mode.label === colorMode.preference,
        );

        if (!selectedMode) return colorModeOptions[0].icon;

        return selectedMode.icon;
    });
</script>

<template>
    <DropdownMenu>
        <DropdownMenuTrigger
            class="size-10 bg-primary rounded-full inline-flex items-center justify-center"
        >
            <Icon :name="icon" class="text-primary-foreground" />
        </DropdownMenuTrigger>
        <DropdownMenuContent>
            <DropdownMenuItem
                v-for="mode in colorModeOptions"
                :key="mode.label"
                @click="mode.action"
            >
                {{ capitalize(mode.label) }}
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>
