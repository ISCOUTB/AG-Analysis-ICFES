<script setup lang="ts">
    import { toTypedSchema } from "@vee-validate/zod";
    import { LoginSchema, formFields } from "@/schemas/auth/login.schema";
    import { useToast } from "@/components/ui/toast";
    import { cn, handleGoRoot } from "@/lib/utils";
    import { providers } from "@/lib/providers";

    interface SheetSavedAnalysisProvider {
        icon: string;
        label: string;
        action: () => unknown;
    }

    const validationSchema = toTypedSchema(LoginSchema);

    const { handleSubmit, errors } = useForm({
        validationSchema,
        initialValues: {
            email: "",
            password: "",
        },
    });

    const { toast } = useToast();
    const { fetch } = useUserSession();
    const { parsedData, reload } = useSavedAnalysis();

    const providerItems: SheetSavedAnalysisProvider[] = providers.map(
        ({ label, redirectTo }) => {
            return {
                label,
                action: () =>
                    navigateTo({ path: redirectTo }, { external: true }),
                icon: `mdi:${label}`,
            };
        },
    );

    const onSubmit = handleSubmit((values) => {
        const { email, password } = values;

        $fetch("/api/auth/login", {
            method: "POST",
            body: { email, password },
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        }).then(async () => {
            toast({
                title: "Logged In!",
            });

            await fetch();

            handleGoRoot();
        });
    });
</script>

<template>
    <AuthState v-slot="{ loggedIn }">
        <Sheet>
            <SheetTrigger as-child>
                <Button variant="outline" @click="reload">
                    Show stored analysis
                </Button>
            </SheetTrigger>
            <SheetContent class="overflow-y-auto overflow-x-hidden">
                <template v-if="loggedIn">
                    <SheetHeader>
                        <SheetTitle>Stored Analysis</SheetTitle>
                    </SheetHeader>
                    <div class="flex flex-col gap-4 mt-4">
                        <template v-if="parsedData.length">
                            <SheetSavedAnalysisCollapsible
                                v-for="item in parsedData"
                                :key="item.id"
                                :saved-item="item"
                            />
                        </template>
                        <template v-else>
                            <div
                                class="text-sm text-purple-500 dark:text-rose-500 underline"
                            >
                                The current user haven't saved any analysis yet
                            </div>
                        </template>
                    </div>
                </template>
                <template v-else>
                    <SheetHeader>
                        <SheetTitle>Access Denied</SheetTitle>
                        <SheetDescription
                            >You're not logged in. Let's fix
                            that!</SheetDescription
                        >
                    </SheetHeader>
                    <div class="mt-4 flex flex-col gap-2">
                        <form class="space-y-6" @submit="onSubmit">
                            <FormField
                                v-for="field in formFields"
                                v-slot="{ componentField }"
                                :key="field.name"
                                :name="field.name"
                            >
                                <FormItem>
                                    <FormLabel
                                        :class="
                                            cn({
                                                'dark:text-foreground':
                                                    errors[field.name],
                                            })
                                        "
                                    >
                                        {{ field.label }}
                                    </FormLabel>
                                    <FormControl>
                                        <Input
                                            :type="field.type"
                                            v-bind="componentField"
                                            :autocomplete="field.autocomplete"
                                            :class="
                                                cn('dark:bg-gray-700', {
                                                    'border-rose-500 dark:border-orange-400 border-2':
                                                        errors[field.name],
                                                })
                                            "
                                        />
                                    </FormControl>
                                    <FormMessage class="dark:text-orange-400" />
                                </FormItem>
                            </FormField>
                        </form>

                        <Button class="w-full mt-2"> Log In </Button>
                        <Separator label="or" class="mt-2" />

                        <div>
                            <span
                                class="text-sm block text-gray-500 text-center"
                                >Continue with</span
                            >
                            <div class="flex gap-1 flex-wrap mt-2">
                                <Button
                                    v-for="item in providerItems"
                                    :key="item.label"
                                    class="flex-grow text-2xl py-1"
                                    variant="outline"
                                    @click="item.action"
                                >
                                    <Icon :name="item.icon" />
                                </Button>
                            </div>
                        </div>

                        <div class="mt-4">
                            <span class="text-sm"
                                >Don't have an account?
                                <NuxtLink
                                    to="/auth/register"
                                    class="text-orange-500 dark:text-slate-200 font-bold"
                                    >Register</NuxtLink
                                ></span
                            >
                        </div>
                    </div>
                </template>
            </SheetContent>
        </Sheet>
    </AuthState>
</template>
