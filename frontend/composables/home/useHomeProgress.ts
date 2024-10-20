import { ReportType } from "~/types/types";

export default async function () {
    const { highschoolStudentsData, collegeStudentsData, studentsCount } =
        await useStudents();
    const store = useAnalysisOptions();
    const progress = computed<number>(() => {
        if (store.reportType === ReportType.SABER11) {
            return (
                (highschoolStudentsData.value.length / studentsCount.value) *
                100
            );
        }

        if (store.reportType === ReportType.SABERPRO) {
            return (
                (collegeStudentsData.value.length / studentsCount.value) * 100
            );
        }

        return 0;
    });

    return {
        progress,
    };
}
