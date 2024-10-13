import { useAnalysisOptions } from "@/stores/analysisOptions";
import { ReportType, StudentsCountStatus } from "@/types/types";
import type { CollegeStudentsQuery, HighschoolStudentsQuery } from "#gql";
import { useToast } from "@/components/ui/toast";

enum Status {
    IDLE,
    LOADING,
    COMPLETED,
    ERROR,
}

type HighschoolStudent = NonNullable<
    NonNullable<HighschoolStudentsQuery["highschoolStudents"]>[number]
>;

type CollegeStudent = NonNullable<
    NonNullable<CollegeStudentsQuery["collegeStudents"]>[number]
>;

function calculatePageSize(x: number): number {
    return Math.max(x / Math.pow(Math.log(x), 2), 100);
}

// function filterData<T>(array: (T | null | undefined)[]): T[] {
//     return array.filter(
//         (item): item is T => item !== null && item !== undefined,
//     );
// }

export default async function () {
    const store = useAnalysisOptions();
    const { department, municipality, institution } = storeToRefs(store);
    const { toast } = useToast();

    const status = useState<Status>(() => Status.IDLE);
    // const error = useState<unknown>();

    const calculatedPageSize = computed(() =>
        calculatePageSize(store.studentsCount),
    );

    const totalPages = computed(() =>
        Math.ceil(store.studentsCount / calculatedPageSize.value),
    );

    const highschoolStudentsData = useState<HighschoolStudent[]>(
        "highschool-students-data",
        () => [],
    );

    const collegeStudentsData = useState<CollegeStudent[]>(
        "college-students-data",
        () => [],
    );

    async function execute() {
        if (store.studentsCountStatus === StudentsCountStatus.LOADING) {
            toast({
                title: "Oops!",
                description:
                    "Students count still loading. Please wait a little ^^",
            });

            return;
        }

        status.value = Status.LOADING;

        if (store.reportType === ReportType.SABER11) {
            Promise.all(
                Array.from({ length: totalPages.value }).map((_, pageIndex) => {
                    return GqlHighschoolStudents({
                        departmentId: department.value,
                        municipalityId: municipality.value,
                        highschoolId: institution.value,
                        pageSize: calculatedPageSize.value,
                        page: pageIndex + 1,
                    });
                }),
            )
                .then((data) => console.table(data))
                // .then(
                //     (combinedData) =>
                //         (highschoolStudentsData.value =
                //             filterData(combinedData)),
                // )
                // .catch((_error) => {
                //     error.value = _error;
                //     status.value = Status.ERROR;
                // })
                .finally(() => (status.value = Status.COMPLETED));
        }

        if (store.reportType === ReportType.SABERPRO) {
            Promise.all(
                Array.from({ length: totalPages.value }).map((_, pageIndex) => {
                    return GqlCollegeStudents({
                        departmentId: department.value,
                        municipalityId: municipality.value,
                        collegeId: institution.value,
                        pageSize: calculatedPageSize.value,
                        page: pageIndex + 1,
                    });
                }),
            )
                .then((data) => console.log(data))
                // .then(
                //     (combinedData) =>
                //         (collegeStudentsData.value = filterData(combinedData)),
                // )
                // .catch((_error) => {
                //     error.value = _error;
                //     status.value = Status.ERROR;
                // })
                .finally(() => (status.value = Status.COMPLETED));
        }
    }

    return {
        status,
        highschoolStudentsData,
        collegeStudentsData,
        execute,
    };
}
