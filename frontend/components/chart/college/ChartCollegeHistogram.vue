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
    const { skewness, kurtosis } = useStatistics();

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

    const dataArray = computed(() => {
        if (!categorizedData.value) return [];

        return categorizedData.value.map(({ count }) => count);
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
            <Table>
                <TableHeader>
                    <TableHead>Test</TableHead>
                    <TableHead>Value</TableHead>
                </TableHeader>
                <TableBody>
                    <TableRow>
                        <TableCell>Skewness</TableCell>
                        <TableCell>{{ skewness(dataArray) }}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Kurtosis</TableCell>
                        <TableCell>{{ kurtosis(dataArray) }}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </template>
    </template>
</template>
