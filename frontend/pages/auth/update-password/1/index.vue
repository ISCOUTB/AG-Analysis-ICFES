<script setup lang="ts">
    import { z } from "zod";
    import { cn, handleGoBack, handleGoRoot } from "@/lib/utils";
    import { useToast } from "@/components/ui/toast";
    import { useUpdatePassword } from "@/stores/updatePassword";

    const schema = z.object({
        password: z
            .string()
            .min(1, { message: "Your current password is required" }),
    });

    const validationSchema = toTypedSchema(schema);
    const { handleSubmit, errors } = useForm({
        validationSchema,
        initialValues: {
            password: "",
        },
    });

    const { toast } = useToast();

    const formFields: FormField<z.infer<typeof schema>>[] = [
        {
            name: "password",
            type: "password",
            label: "Current Password",
            autocomplete: "current-password",
        },
    ];

    const onSubmit = handleSubmit((values) => {
        $fetch("/api/auth/user/valid-password", {
            method: "POST",
            body: { password: values.password },
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        }).then(async () => {
            const { markAsCompleted } = useUpdatePassword();

            markAsCompleted("1");

            await navigateTo({ path: "/auth/update-password/2" });
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
                    Change Password
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
