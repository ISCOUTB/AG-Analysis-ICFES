<script setup lang="ts">
    import { providers } from "@/lib/providers";
    import { createAvatarFallback } from "@/lib/utils";
    import { capitalize } from "vue";
    import { useToast } from "@/components/ui/toast";

    interface DropdownMenuItem {
        label: string;
        icon?: string;
        action?: () => unknown;
        subItems?: DropdownMenuItem[];
    }

    const { clear } = useUserSession();
    const { toast } = useToast();

    const dropdownMenuItems: DropdownMenuItem[] = [
        {
            label: "Sign up",
            subItems: [
                {
                    label: "Login",
                    icon: "mdi:login",
                    action: async () =>
                        await navigateTo({ path: "/auth/login" }),
                },
                ...providers.map(({ label, redirectTo }) => {
                    return {
                        label,
                        action: () =>
                            navigateTo(
                                { path: redirectTo },
                                { external: true },
                            ),
                        icon: `mdi:${label}`,
                    };
                }),
            ],
        },
        {
            label: "Edit Account",
            action: async () => await navigateTo({ path: "/auth/edit" }),
        },
        {
            label: "Sign out",
            action: async () => {
                clear();
                toast({
                    title: "Logged out",
                });

                await navigateTo({ path: "/" });
            },
        },
    ];
</script>

<template>
    <AuthState>
        <template #default="{ user }">
            <DropdownMenu>
                <DropdownMenuTrigger>
                    <Avatar
                        size="sm"
                        class="border border-gray-950 dark:border-none"
                    >
                        <AvatarImage :src="user?.image || '/default.jpg'" />
                        <AvatarFallback>
                            {{ createAvatarFallback(user?.name) }}
                        </AvatarFallback>
                    </Avatar>
                </DropdownMenuTrigger>
                <DropdownMenuContent class="w-64">
                    <DropdownMenuItem v-if="user">
                        <div class="flex flex-col">
                            <span class="text-xs">Signed as</span>
                            <span v-if="user.name" class="font-semibold">{{
                                user.name
                            }}</span>
                            <span v-if="user.email" class="text-sm">{{
                                user.email
                            }}</span>
                        </div>
                    </DropdownMenuItem>

                    <template v-for="item in dropdownMenuItems">
                        <DropdownMenuItem
                            v-if="!item.subItems"
                            :key="item.label"
                            @click="item.action"
                        >
                            {{ capitalize(item.label) }}
                        </DropdownMenuItem>
                        <DropdownMenuSub v-else :key="item.subItems[0].label">
                            <DropdownMenuSubTrigger>
                                {{ capitalize(item.label) }}
                            </DropdownMenuSubTrigger>
                            <DropdownMenuPortal>
                                <DropdownMenuSubContent>
                                    <DropdownMenuItem
                                        v-for="subItem in item.subItems"
                                        :key="subItem.label"
                                        @click="subItem.action"
                                    >
                                        <div class="flex items-center gap-2">
                                            <Icon
                                                v-if="subItem.icon"
                                                :name="subItem.icon"
                                                class="text-lg"
                                            />
                                            <span>{{
                                                capitalize(subItem.label)
                                            }}</span>
                                        </div>
                                    </DropdownMenuItem>
                                </DropdownMenuSubContent>
                            </DropdownMenuPortal>
                        </DropdownMenuSub>
                    </template>
                </DropdownMenuContent>
            </DropdownMenu>
        </template>
    </AuthState>
</template>
