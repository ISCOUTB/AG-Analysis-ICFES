<!-- TODO -->
<!-- 1. Now that the key is selected, generate the histogram -->

<script setup lang="ts">
    import {
        HighschoolDataSchemaArray,
        type HighschoolDataKeys,
    } from "@/schemas/analysis/students.schema";

    const { highschoolCategories } = await useStudentsData();
    const { data } = useSelectedData();
    const parsedData = computed(() => {
        if (!Array.isArray(data.value) || !data.value.length) return [];

        return HighschoolDataSchemaArray.parse(data.value);
    });
    const selectedSubject = useState<HighschoolDataKeys>();

    const categorizedData = computed<HistogramChartData[] | undefined>(() => {
        if (!selectedSubject.value) return;

        return createRanges({ min: 0, max: 100, steps: 10 }).map(
            ({ minRange, maxRange }) => {
                return {
                    minRange,
                    maxRange,
                    label: `[${minRange}, ${maxRange}]`,
                    count: parsedData.value.filter(
                        (student) =>
                            student[selectedSubject.value] >= minRange &&
                            student[selectedSubject.value] <= maxRange,
                    ).length,
                };
            },
        );
    });
</script>

<template>
    <template v-if="parsedData.length">
        <ToggleGroup
            type="single"
            class="flex flex-wrap rounded-lg border-2 border-gray-300/30 dark:border-gray-400/20 py-2"
        >
            <ToggleGroupItem
                v-for="item in highschoolCategories"
                :key="item"
                :value="item"
                class="font-semibold"
                @click="selectedSubject = item"
            >
                {{ item }}
            </ToggleGroupItem>
        </ToggleGroup>
        <pre>
            {{ categorizedData }}
        </pre>
    </template>
</template>
