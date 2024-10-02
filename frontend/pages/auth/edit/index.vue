<script setup lang="ts">
    import type { z } from "zod";
    import { UpdateSchema } from "@/schemas/auth/update.schema";
    import { cn, handleGoBack, handleGoRoot } from "@/lib/utils";
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Edit Account",
    });

    definePageMeta({
        middleware: ["auth"],
    });

    const validationSchema = toTypedSchema(UpdateSchema);

    const { session, fetch } = useUserSession();
    const { handleSubmit, errors } = useForm({
        validationSchema,
        initialValues: {
            email: session.value.user?.email,
            username: session.value.user?.name,
        },
    });
    const { toast } = useToast();

    const formFields: FormField<z.infer<typeof UpdateSchema>>[] = [
        {
            name: "email",
            label: "Email",
            type: "email",
            autocomplete: "email",
        },
        {
            name: "username",
            label: "Username",
            type: "text",
            autocomplete: "username",
        },
    ];

    const onSubmit = handleSubmit((values) => {
        if (!session.value.user) return;

        const { username: newUsername, email: newEmail } = values;
        const { name, email } = session.value.user;

        if (name === newUsername && email === newEmail) return;

        $fetch("/api/auth/user/edit", {
            method: "POST",
            body: {
                name: newUsername,
                email: newEmail,
            },
            query: {
                userId: session.value.user.id,
            },
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        }).then(async () => {
            toast({
                title: "User updated!",
            });

            await fetch();

            handleGoRoot();
        });
    });
</script>

<template>
    <section :key="$route.fullPath" class="w-full bg-background py-12">
        <Card class="max-w-3xl container dark:bg-gray-800">
            <CardHeader>
                <CardTitle
                    class="text-2xl font-bold text-center dark:text-gray-100"
                >
                    Update
                </CardTitle>
            </CardHeader>
            <CardContent>
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

                    <div>
                        <NuxtLink
                            to="/auth/update-password/1"
                            class="text-orange-500 text-sm dark:text-slate-200 font-bold"
                            >Change password</NuxtLink
                        >
                    </div>

                    <div class="space-x-2">
                        <Button
                            type="button"
                            variant="outline"
                            @click="handleGoBack"
                            >Go Back</Button
                        >
                        <Button
                            type="button"
                            variant="destructive"
                            class="dark:bg-orange-500"
                            @click="handleGoRoot"
                        >
                            Cancel
                        </Button>
                        <Button type="submit"> Submit </Button>
                    </div>
                </form>
            </CardContent>
        </Card>
    </section>
</template>
