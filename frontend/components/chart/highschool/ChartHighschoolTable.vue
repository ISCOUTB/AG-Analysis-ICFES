<script setup lang="ts">
    import type { HighschoolDataSchemaType } from "@/schemas/analysis/students.schema";
    import { std, variance, quantileSeq } from "mathjs";

    const { parsedHighschoolStudentsData, highschoolCategories } =
        await useStudentsData();

    const tableData = computed<TableData[]>(() =>
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
            std: roundToDecimals(Number(std(values)), 2),
            variance: roundToDecimals(Number(variance(values)), 2),
            Q1: quantileSeq(values, 0.25),
            Q3: quantileSeq(values, 0.75),
            median: quantileSeq(values, 0.5),
        };
    }
</script>

<template>
    <div class="space-y-6">
        <Separator label="Descriptive Variables" />
        <ChartDescription class="text-center">
            Standard Deviation, Variance, Q1, Q3 and Median for each subject.
        </ChartDescription>
        <Table>
            <TableHeader>
                <TableHead> Subject </TableHead>
                <TableHead>Standard Deviation</TableHead>
                <TableHead>Variance</TableHead>
                <TableHead>Q1</TableHead>
                <TableHead>Q3</TableHead>
                <TableHead>Median</TableHead>
            </TableHeader>
            <TableBody>
                <TableRow v-for="item in tableData" :key="item.name">
                    <TableCell class="font-bold">
                        {{ item.name }}
                    </TableCell>
                    <TableCell>{{ item.std }}</TableCell>
                    <TableCell>{{ item.variance }}</TableCell>
                    <TableCell>{{ item.Q1 }}</TableCell>
                    <TableCell>{{ item.Q3 }}</TableCell>
                    <TableCell>{{ item.median }}</TableCell>
                </TableRow>
            </TableBody>
        </Table>
    </div>
</template>
