<script setup lang="ts">
    import { z } from "zod";
    import type { HighschoolResponseArray } from "@/schemas/analysis/students.schema";
    import { ChevronsUpDown } from "lucide-vue-next";

    interface Props {
        highschoolId: string;
        items: Record<string, z.infer<typeof HighschoolResponseArray>>;
    }

    const { highschoolId, items } = defineProps<Props>();

    const HighschoolResponse = z.object({
        id: z.number(),
        name: z.string(),
    });

    const PeriodResponse = z.object({
        id: z.number(),
        label: z.string(),
    });

    const { $api } = useNuxtApp();

    const [_, highschoolResponse] = await withCatch(
        $api<unknown>(`/highschool/${highschoolId}`),
    );
    const highschool = HighschoolResponse.parse(highschoolResponse);

    const periods = await Promise.all(
        Object.keys(items).map(async (period) => {
            const [_, response] = await withCatch(
                $api<unknown>(`/period/${period}`),
            );

            return PeriodResponse.parse(response);
        }),
    );
</script>

<template>
    <Collapsible>
        <div
            class="flex items-center justify-between mr-4 px-4 py-1 rounded-md"
        >
            <div class="flex flex-col items-start">
                <h4 class="text-sm font-semibold">
                    {{ highschool.name }}
                </h4>
            </div>

            <div>
                <CollapsibleTrigger as-child>
                    <Button variant="ghost" size="sm" class="w-9 p-0">
                        <ChevronsUpDown class="h-4 w-4" />
                        <span class="sr-only">Toggle</span>
                    </Button>
                </CollapsibleTrigger>
            </div>
        </div>
        <CollapsibleContent class="px-4">
            <div v-for="item in periods" :key="item.id">{{ item.label }}</div>
        </CollapsibleContent>
    </Collapsible>
</template>
