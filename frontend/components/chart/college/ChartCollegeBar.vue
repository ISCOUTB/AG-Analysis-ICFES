<script setup lang="ts">
    import type { CollegeDataSchemaType } from "@/schemas/analysis/students.schema";

    const { parsedCollegeStudentsData, collegeCategories } =
        await useStudentsData();

    const chartData = computed<BarChartData[]>(() =>
        collegeCategories.value.map((category) => ({
            name: category,
            ...calculateStats(category),
        })),
    );

    function calculateStats(key: keyof CollegeDataSchemaType) {
        const values = parsedCollegeStudentsData.value.map((item) => item[key]);
        return {
            average: roundToDecimals(
                values.reduce((acc, val) => acc + val, 0) / values.length,
                2,
            ),
            max: Math.max(...values),
            min: Math.min(...values),
        };
    }
</script>

<template>
    <div class="space-y-4">
        <Separator label="College Chart Bar" />
        <ChartDescription class="text-center">
            Basic description of the sample data. Showing max, min, and the
            average of them.
        </ChartDescription>
        <BarChart
            :data="chartData"
            index="name"
            :categories="['max', 'min', 'average']"
            :rounded-corners="4"
        />
    </div>
</template>
