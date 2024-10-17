<script setup lang="ts">
    import { z } from "zod";

    const { collegeStudentsData } = await useStudents();

    const DataSchema = z.object({
        MOD_QUANTITATIVE_REASONING: z.number(),
        MOD_WRITTEN_COMMUNICATION: z.number(),
        MOD_CRITICAL_READING: z.number(),
        MOD_ENGLISH: z.number(),
        MOD_CITIZENSHIP_COMPETENCES: z.number(),
    });

    type DataSchemaType = z.infer<typeof DataSchema>;

    const parsedData = computed(() =>
        collegeStudentsData.value.map((item) => DataSchema.parse(item)),
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
