<script setup lang="ts">
    import type { HighschoolDataSchemaType } from "@/schemas/analysis/students.schema";

    const { parsedHighschoolStudentsData, highschoolCategories } =
        await useStudentsData();

    const chartData = computed<BarChartData[]>(() =>
        highschoolCategories.value.map((category) => ({
            name: category,
            ...calculateStats(category),
        })),
    );

    function calculateStats(key: keyof HighschoolDataSchemaType) {
        const values = parsedHighschoolStudentsData.value.map(
            (item) => item[key],
        );
        
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
    <div class="space-y-2">
        <Separator label="Highschool Chart Bar" />
        <BarChart
            :data="chartData"
            index="name"
            :categories="['max', 'min', 'average']"
            :rounded-corners="4"
        />
    </div>
</template>
