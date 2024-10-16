<script setup lang="ts">
    import { Check } from "lucide-vue-next";
    import { STUDENTS_CHUNK_SIZE } from "~/config/constants";

    useHead({
        title: "Pricing",
    });

    const items: PricingPlan[] = [
        {
            title: "Basic",
            description: "Perfect for individuals and small teams",
            price: "$9.99",
            features: [
                "5 Projects",
                "Basic Analysis",
                `${STUDENTS_CHUNK_SIZE} students x 100 Requests`,
            ],
            message: "Current Plan",
            disabled: true,
        },
        {
            title: "Pro",
            description: "Ideal for growing businesses",
            price: "$19.99",
            features: [
                "Unlimited projects",
                "Advanced Analysis",
                "Priority Support",
                `${STUDENTS_CHUNK_SIZE} students x 10000 Requests`,
            ],
            message: "Get Started",
            disabled: false,
        },
        {
            title: "Enterprise",
            description: "For large organizations with specific needs",
            price: "Custom",
            features: [
                "Custom solutions",
                "Dedicated account manager",
                "Advanced security features",
                "Unlimited students requests",
            ],
            message: "Contact Sales",
            disabled: false,
        },
    ];
</script>

<template>
    <section :key="$route.fullPath" class="w-full bg-background py-12">
        <div class="container px-4 md:px-6">
            <div class="flex flex-col gap-2">
                <span class="text-3xl font-bold text-gray-900"
                    >Choose your plan</span
                >
                <span class="text-lg text-gray-600"
                    >Select the perfect plan for your needs and start analyzing
                    today.</span
                >
            </div>

            <div class="mt-12 flex flex-col lg:grid lg:grid-cols-3 gap-4">
                <Card v-for="item in items" :key="item.title">
                    <CardHeader>
                        <CardTitle>{{ item.title }}</CardTitle>
                        <CardDescription>{{
                            item.description
                        }}</CardDescription>
                    </CardHeader>
                    <CardContent class="flex-grow">
                        <p class="text-4xl font-bold mb-4">{{ item.price }}</p>
                        <ul class="h-32">
                            <li
                                v-for="feature in item.features"
                                :key="feature"
                                class="flex items-center"
                            >
                                <Check class="size-5 text-green-500 mr-2" />
                                <span class="text-gray-800">
                                    {{ feature }}
                                </span>
                            </li>
                        </ul>
                    </CardContent>
                    <CardFooter>
                        <Button :disabled="item.disabled" class="w-full">{{
                            item.message
                        }}</Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
    </section>
</template>
