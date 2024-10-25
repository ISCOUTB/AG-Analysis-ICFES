<script setup lang="ts">
    import { z } from "zod";
    import type { CollegeResponseArray } from "@/schemas/analysis/students.schema";
    import { ChevronsUpDown } from "lucide-vue-next";
    import { useToast } from "@/components/ui/toast";

    interface Props {
        collegeId: string;
        items: Record<string, z.infer<typeof CollegeResponseArray>>;
    }

    const { collegeId, items } = defineProps<Props>();

    const CollegeResponse = z.object({
        id: z.number(),
        name: z.string(),
    });

    const PeriodResponse = z.object({
        id: z.number(),
        label: z.string(),
    });

    const { $api } = useNuxtApp();
    const { toast } = useToast();
    const { data } = useSelectedData();
    const isOpen = ref<boolean>(false);

    const [_, collegeResponse] = await withCatch(
        $api<unknown>(`/college/${collegeId}`),
    );
    const college = CollegeResponse.parse(collegeResponse);

    const periods = await Promise.all(
        Object.keys(items).map(async (period) => {
            const [_, response] = await withCatch(
                $api<unknown>(`/period/${period}`),
            );

            return PeriodResponse.parse(response);
        }),
    );

    function handleSelect({ periodId }: { periodId: number }) {
        if (!Object.keys(items).some((key) => key === periodId.toString())) {
            toast({
                title: "Oops! Wrong key",
            });

            return;
        }

        data.value = items[periodId];

        const period = periods.filter((item) => item.id === periodId)[0];

        isOpen.value = false;

        toast({
            title: "Selected",
            description: `Institution: ${college.name} with ${period.label} period`,
        }); 

        scrollToElement("component__toggle-group__histogram-college");
    }
</script>

<template>
    <Collapsible v-model:open="isOpen">
        <div
            class="flex items-center justify-between mr-4 px-4 py-1 rounded-md"
        >
            <div class="flex flex-col items-start">
                <h4 class="text-sm font-semibold">
                    {{ college.name }}
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
            <div
                v-for="item in periods"
                :key="item.id"
                class="border-b-2 border-gray-300/30 dark:border-gray-400/20 py-2 pr-4 flex justify-between items-center"
            >
                <span class="font-bold text-gray-800 dark:text-gray-200">
                    {{ item.label }}
                </span>
                <Button @click="handleSelect({ periodId: item.id })">
                    Select
                </Button>
            </div>
        </CollapsibleContent>
    </Collapsible>
</template>
