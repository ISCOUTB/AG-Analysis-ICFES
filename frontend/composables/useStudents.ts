import { useAnalysisOptions } from "@/stores/analysisOptions";
import { ReportType, StudentsCountStatus, Status } from "@/types/types";
import { useToast } from "@/components/ui/toast";
import { z } from "zod";

function calculatePageSize(x: number): number {
    return Math.max(Math.ceil(x / Math.pow(Math.log(x), 2)), 100);
}

const HighschoolResponse = z.object({
    id: z.number(),
    genre: z.string(),
    PUNT_ENGLISH: z.number(),
    PUNT_MATHEMATICS: z.number(),
    PUNT_SOCIAL_CITIZENSHIP: z.number(),
    PUNT_NATURAL_SCIENCES: z.number(),
    PUNT_CRITICAL_READING: z.number(),
    PUNT_GLOBAL: z.number(),
    period: z.number(),
    highschool: z.number(),
});

const HighschoolResponseArray = z.array(HighschoolResponse);

const CollegeResponse = z.object({
    id: z.number(),
    genre: z.string(),
    MOD_QUANTITATIVE_REASONING: z.number(),
    MOD_WRITTEN_COMMUNICATION: z.number(),
    MOD_CRITICAL_READING: z.number(),
    MOD_ENGLISH: z.number(),
    MOD_CITIZENSHIP_COMPETENCES: z.number(),
    period: z.number(),
    college: z.number(),
});

const CollegeResponseArray = z.array(CollegeResponse);

export default async function () {
    const store = useAnalysisOptions();
    const { toast } = useToast();
    const { $api } = useNuxtApp();

    const status = useState<Status>(() => Status.IDLE);
    const error = useState<unknown>();

    const calculatedPageSize = computed(() =>
        calculatePageSize(store.studentsCount),
    );

    const totalPages = computed(() =>
        Math.ceil(store.studentsCount / calculatedPageSize.value),
    );

    const highschoolStudentsData =
        useState<z.infer<typeof HighschoolResponseArray>>();

    const collegeStudentsData =
        useState<z.infer<typeof CollegeResponseArray>>();

    async function execute() {
        console.log(totalPages.value, calculatedPageSize.value);

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
                Array.from({ length: totalPages.value }).map(
                    async (_, pageIndex) => {
                        const response = await $api<unknown[]>(
                            "/highschool/students_paginated/",
                            {
                                method: "POST",
                                body: {
                                    department: store.department,
                                    municipality: store.municipality,
                                    highschool: store.institution,
                                    period: store.period,
                                    page: pageIndex + 1,
                                    pageSize: calculatedPageSize,
                                },
                            },
                        );

                        return HighschoolResponseArray.parse(response);
                    },
                ),
            )
                .then((data) => data.flat(Infinity))
                .then((data) => console.table(data))
                .catch((_error) => {
                    error.value = _error;
                    status.value = Status.ERROR;
                })
                .finally(() => (status.value = Status.COMPLETED));
        }

        if (store.reportType === ReportType.SABERPRO) {
            Promise.all(
                Array.from({ length: totalPages.value }).map(
                    async (_, pageIndex) => {
                        const response = await $api<unknown[]>(
                            "/college/students_paginated/",
                            {
                                method: "POST",
                                body: {
                                    department: store.department,
                                    municipality: store.municipality,
                                    college: store.institution,
                                    period: store.period,
                                    page: pageIndex + 1,
                                    pageSize: calculatedPageSize,
                                },
                            },
                        );

                        return CollegeResponseArray.parse(response);
                    },
                ),
            )
                .then((data) => console.log(data))
                .catch((_error) => {
                    error.value = _error;
                    status.value = Status.ERROR;
                })
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
