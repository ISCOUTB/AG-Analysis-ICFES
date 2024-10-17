import {
    HighschoolDataSchema,
    CollegeDataSchema,
    type HighschoolDataSchemaType,
    type CollegeDataSchemaType,
} from "@/schemas/analysis/students.schema";

export default async function () {
    const { highschoolStudentsData, collegeStudentsData } = await useStudents();

    const parsedHighschoolStudentsData = computed(() =>
        highschoolStudentsData.value.map((item) =>
            HighschoolDataSchema.parse(item),
        ),
    );

    const parsedCollegeStudentsData = computed(() =>
        collegeStudentsData.value.map((item) => CollegeDataSchema.parse(item)),
    );

    const highschoolCategories = computed(
        () =>
            Object.keys(
                parsedHighschoolStudentsData.value[0],
            ) as (keyof HighschoolDataSchemaType)[],
    );

    const collegeCategories = computed(
        () =>
            Object.keys(
                parsedCollegeStudentsData.value[0],
            ) as (keyof CollegeDataSchemaType)[],
    );

    return {
        parsedHighschoolStudentsData,
        parsedCollegeStudentsData,
        highschoolCategories,
        collegeCategories,
    };
}
