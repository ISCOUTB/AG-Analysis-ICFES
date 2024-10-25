export default async function () {
    const { execute, highschoolStudentsData, collegeStudentsData } =
        await useStudents();

    highschoolStudentsData.value.length = 0;
    collegeStudentsData.value.length = 0;
    execute();
}
