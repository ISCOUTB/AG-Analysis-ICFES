<script setup lang="ts">
    import {
        CollegeDataSchemaArray,
        type CollegeDataKeys,
    } from "@/schemas/analysis/students.schema";

    const { collegeCategories } = await useStudentsData();
    const { data } = useSelectedData();
    const parsedData = computed(() => {
        if (!Array.isArray(data.value) || !data.value.length) return [];

        return CollegeDataSchemaArray.parse(data.value);
    });
    const selectedSubject = useState<CollegeDataKeys>();

    const categorizedData = computed<HistogramChartData[] | undefined>(() => {
        if (!selectedSubject.value) return;

        return createRanges({ min: 0, max: 100, steps: 10 }).map(
            ({ minRange, maxRange }) => {
                return {
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
        <Separator label="Select Subject" />

        <ToggleGroup
            type="single"
            class="flex flex-wrap rounded-lg border-2 border-gray-300/30 dark:border-gray-400/20 py-2"
        >
            <ToggleGroupItem
                v-for="item in collegeCategories"
                :key="item"
                :value="item"
                class="font-semibold"
                @click="selectedSubject = item"
            >
                {{ item }}
            </ToggleGroupItem>
        </ToggleGroup>

        <template v-if="categorizedData">
            <BarChart
                :data="categorizedData"
                :categories="['count']"
                index="label"
                :rounded-corners="4"
                :show-grid-line="false"
            />
        </template>
    </template>
</template>
