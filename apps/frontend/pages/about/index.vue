<script setup lang="ts">
    import { createAvatarFallback } from "@/lib/utils";

    interface Participant {
        name: string;
        role: string;
        description: string;
        tags: string[];
        image: string;
    }

    const participants: Participant[] = [
        {
            name: "Mauro Gonzalez",
            role: "Frontend Developer",
            description: "Lorem Ipsum dolor sit amet",
            tags: ["UI Designer", "Vue Developer"],
            image: "https://th.bing.com/th/id/R.fbfb9f15f4cab25264e51d3912f69b1d?rik=O83ol7vxuFN76g&pid=ImgRaw&r=0&sres=1&sresct=1",
        },
    ];
</script>

<template>
    <section :key="$route.fullPath" class="w-full bg-background">
        <div class="container px-4 py-12 flex flex-col gap-4">
            <Card
                v-for="participant in participants"
                :key="participant.name"
                class="flex flex-col w-3/4 mx-auto sm:w-full sm:grid sm:grid-cols-[3fr_2fr] sm:items-center"
            >
                <CardHeader class="flex-row items-center gap-4">
                    <Avatar size="base">
                        <AvatarImage :src="participant.image" />
                        <AvatarFallback>
                            {{ createAvatarFallback(participant.name) }}
                        </AvatarFallback>
                    </Avatar>

                    <div class="flex flex-col gap-1">
                        <CardTitle>
                            {{ participant.name }}
                        </CardTitle>
                        <CardDescription>
                            {{ participant.description }}
                        </CardDescription>
                    </div>
                </CardHeader>
                <CardContent
                    class="h-full flex flex-wrap items-start gap-2 sm:py-8"
                >
                    <span
                        v-for="tag in participant.tags"
                        :key="tag"
                        class="text-sm rounded-full bg-gray-950 text-slate-50 dark:bg-slate-50 dark:text-gray-950 font-semibold px-4 py-1"
                    >
                        {{ tag }}
                    </span>
                </CardContent>
            </Card>
        </div>
    </section>
</template>
