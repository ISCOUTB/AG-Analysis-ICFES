<!-- <script setup lang="ts">
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

    function calculateStats(key: keyof DataSchemaType) {
        const values = parsedData.value.map((item) => item[key]);
    }
</script> -->
