<script setup lang="ts">
    import { z } from "zod";

    const { highschoolStudentsData } = await useStudents();

    const DataSchema = z.object({
        PUNT_ENGLISH: z.number(),
        PUNT_MATHEMATICS: z.number(),
        PUNT_SOCIAL_CITIZENSHIP: z.number(),
        PUNT_NATURAL_SCIENCES: z.number(),
        PUNT_CRITICAL_READING: z.number(),
    });

    type DataSchemaType = z.infer<typeof DataSchema>;

    const parsedData = computed(() =>
        highschoolStudentsData.value.map((item) => DataSchema.parse(item)),
    );

    const categories = computed(
        () => Object.keys(parsedData.value[0]) as (keyof DataSchemaType)[],
    );

    const chartData = computed<BarChartData[]>(() =>
        categories.value.map((category) => ({
            name: category,
            ...calculateStats(category),
        })),
    );

    function calculateStats(key: keyof DataSchemaType) {
        const values = parsedData.value.map((item) => item[key]);
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
    <BarChart
        :data="chartData"
        index="name"
        :categories="['max', 'min', 'average']"
        :rounded-corners="4"
    />
</template>
