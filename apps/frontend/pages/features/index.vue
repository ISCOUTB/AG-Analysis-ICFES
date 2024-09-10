<script setup lang="ts">
    interface KeyFeature {
        icon: string;
        title: string;
        description: string;
    }

    interface FeatureSpotlight {
        label: string;
    }

    interface Feature {
        title: string;
        description: string;
    }

    const keyFeatures: KeyFeature[] = [
        {
            icon: "mdi:google",
            title: "Reliable",
            description: "Lorem ipsum dolor si amet",
        },
        {
            icon: "mdi:google",
            title: "Reliable",
            description: "Lorem ipsum dolor si amet",
        },
        {
            icon: "mdi:google",
            title: "Reliable",
            description: "Lorem ipsum dolor si amet",
        },
    ];

    const featureSpotlight: FeatureSpotlight[] = [
        { label: "Lorem Ipsum" },
        { label: "Lorem Ipsum" },
        { label: "Lorem Ipsum" },
    ];

    const features: Feature[] = [
        {
            title: "Feature",
            description:
                "Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis, vel similique laborum perferendis qui obcaecati et culpa pariatur il enim vitae, debitis soluta nostrum tempora, delectus magni necessitatibus alias assumenda.",
        },
        {
            title: "Feature",
            description:
                "Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis, vel similique laborum perferendis qui obcaecati et culpa pariatur il enim vitae, debitis soluta nostrum tempora, delectus magni necessitatibus alias assumenda.",
        },
        {
            title: "Feature",
            description:
                "Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis, vel similique laborum perferendis qui obcaecati et culpa pariatur il enim vitae, debitis soluta nostrum tempora, delectus magni necessitatibus alias assumenda.",
        },
    ];

    function scrollToSection(id: string) {
        const element = document.getElementById(id);

        if (!element) return;

        element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
</script>

<template>
    <section :key="$route.fullPath" class="w-full bg-background">
        <div id="banner" class="w-full bg-gray-400/30 dark:bg-gray-900">
            <div class="container px-4 py-48 flex flex-col items-center gap-8">
                <div class="flex flex-col items-center gap-4">
                    <span class="text-3xl sm:text-5xl font-bold"
                        >Powerfull tools for your success</span
                    >
                    <span class="text-lg font-semibold"
                        >Discover how you can transform your workflow</span
                    >
                </div>
                <Button
                    class="rounded-full"
                    @click="scrollToSection('main-features')"
                >
                    Explore Features
                </Button>
            </div>
        </div>

        <div
            id="main-features"
            class="container px-4 py-36 flex flex-col items-center gap-10"
        >
            <span class="text-3xl font-bold">Key Features</span>
            <div
                class="w-full flex flex-col sm:flex-row gap-12 sm:gap-0 sm:justify-around"
            >
                <div
                    v-for="feature in keyFeatures"
                    :key="feature.title"
                    class="flex flex-col justify-center items-center gap-4"
                >
                    <div
                        class="size-14 rounded-full bg-gray-400/30 inline-flex items-center justify-center"
                    >
                        <Icon
                            :name="feature.icon"
                            class="text-3xl text-gray-700"
                        />
                    </div>
                    <div class="flex flex-col items-center gap-2">
                        <span class="font-bold text-lg">
                            {{ feature.title }}
                        </span>
                        <span class="text-base line-clamp-1">{{
                            feature.description
                        }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div id="spotlight" class="w-full bg-gray-400/20 dark:bg-gray-900">
            <div
                class="container px-4 py-24 flex flex-col sm:grid sm:grid-cols-2 justify-center items-center gap-8 sm:gap-2"
            >
                <div class="flex justify-center">
                    <NuxtImg
                        class="w-3/4 rounded-lg shadow-lg"
                        src="https://images.nightcafe.studio/jobs/oDm9HyXHj3miRUBjwxmD/oDm9HyXHj3miRUBjwxmD--1--syx06.jpg?tr=w-1600,c-at_max"
                    />
                </div>
                <div class="h-full flex flex-col gap-4">
                    <span class="font-bold text-3xl"> Feature Spotlight </span>
                    <span class="text-sm text-gray-800"
                        >Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Deleniti quos voluptates, quam assumenda ex
                        aliquid quidem quod, obcaecati, ab sed minima earum? At,
                        modi facere magni doloribus voluptates cum dolor.</span
                    >
                    <div class="flex flex-col">
                        <div
                            v-for="item in featureSpotlight"
                            :key="item.label"
                            class="flex items-center gap-2"
                        >
                            <Icon
                                name="material-symbols:check"
                                class="text-3xl text-emerald-500"
                            />
                            <span>{{ item.label }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="more-features" class="w-full">
            <div class="container px-4 py-20 flex flex-col items-center gap-12">
                <span class="font-bold text-2xl">More Features</span>
                <div class="flex flex-col sm:grid sm:grid-cols-2 md:grid-cols-3 gap-4 w-full">
                    <Card v-for="feature in features" :key="feature.title">
                        <CardHeader>
                            <CardTitle>
                                {{ feature.title }}
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            {{ feature.description }}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    </section>
</template>

<style lang="css">
    html {
        scroll-behavior: smooth;
    }
</style>
