<script setup lang="ts">
    import { toTypedSchema } from "@vee-validate/zod";
    import { cn, handleGoBack, handleGoRoot } from "@/lib/utils";
    import { RegisterSchema, formFields } from "@/schemas/auth/register.schema";
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Login",
    });

    const validationSchema = toTypedSchema(RegisterSchema);

    const { handleSubmit, errors } = useForm({
        validationSchema,
        initialValues: {
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
        },
    });

    const { toast } = useToast();

    const onSubmit = handleSubmit((values) => {
        const { email, username, password } = values;

        $fetch("/api/auth/register", {
            method: "POST",
            body: { email, username, password },
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        }).then(async () => {
            toast({
                title: "User created succesfully",
            });
            await navigateTo({ path: "/auth/login" });
        });
    });
</script>

<template>
    <section :key="$route.fullPath" class="w-full bg-background py-12">
        <Card class="max-w-3xl container dark:bg-gray-800">
            <CardHeader>
                <CardTitle
                    class="text-2xl font-bold text-center dark:text-gray-100"
                    >Register</CardTitle
                >
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
                        <span class="text-sm"
                            >Already have an account?
                            <NuxtLink
                                to="/auth/login"
                                class="text-orange-500 dark:text-slate-200 font-bold"
                                >Login</NuxtLink
                            ></span
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
