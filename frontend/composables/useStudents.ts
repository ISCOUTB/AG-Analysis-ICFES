import { useAnalysisOptions } from "@/stores/analysisOptions";
import {
    CollegeResponseArray,
    HighschoolResponseArray,
} from "@/schemas/analysis/students.schema";
import type { FetchOptions } from "ofetch";
import { ReportType, Status } from "@/types/types";
import { useToast } from "@/components/ui/toast";
import { z } from "zod";
import { STUDENTS_CHUNK_SIZE } from "@/config/constants";

interface RequestArgs {
    endpoint: string;
    options: FetchOptions<"json">;
    body: Record<string, unknown>;
}

interface Options {
    page: number;
}

export default async function () {
    const store = useAnalysisOptions();
    const { status } = useStatus();
    const { toast } = useToast();
    const studentsCount = useState(() => 0);

    const highschoolStudentsData = useState<
        z.infer<typeof HighschoolResponseArray>
    >(() => []);

    const collegeStudentsData = useState<z.infer<typeof CollegeResponseArray>>(
        () => [],
    );

    async function gatherStudentsCount() {
        const { $api } = useNuxtApp();

        const Response = z.object({
            count: z.number(),
        });

        if (store.reportType === ReportType.SABER11) {
            const [_, response] = await withCatch(
                $api<unknown>("/highschool/students_count/", {
                    method: "POST",
                    body: {
                        department: store.department,
                        municipality: store.municipality,
                        highschool: store.institution,
                        period: store.period,
                    },
                }),
            );

            const responseParsed = Response.parse(response);

            if (!responseParsed) return;

            studentsCount.value = responseParsed.count;

            return;
        }

        if (store.reportType === ReportType.SABERPRO) {
            const [_, response] = await withCatch(
                $api<unknown>("/college/students_count/", {
                    method: "POST",
                    body: {
                        department: store.department,
                        municipality: store.municipality,
                        college: store.institution,
                        period: store.period,
                    },
                }),
            );

            const responseParsed = Response.parse(response);

            if (!responseParsed) return;

            studentsCount.value = responseParsed.count;

            return;
        }
    }

    async function execute() {
        status.value = Status.LOADING;

        await gatherStudentsCount();

        if (!studentsCount.value) {
            toast({
                title: "Oops! An error ocurred",
                description: "Failed to gather students count",
            });

            return;
        }

        console.log(studentsCount.value);

        const totalPages = Math.ceil(studentsCount.value / STUDENTS_CHUNK_SIZE);

        if (store.reportType === ReportType.SABER11) {
            await Promise.all(
                Array.from({ length: totalPages }).map((_, pageIndex) => {
                    return fetchData(
                        {
                            endpoint: "/highschool/students_paginated/",
                            options: {
                                method: "POST",
                            },
                            body: {
                                department: store.department,
                                municipality: store.municipality,
                                highschool: store.institution,
                                period: store.period,
                                pageSize: STUDENTS_CHUNK_SIZE,
                            },
                        },
                        { page: pageIndex + 1 },
                    )
                        .then((response) =>
                            HighschoolResponseArray.parse(response),
                        )
                        .then((data) => {
                            if (data.length) {
                                highschoolStudentsData.value = [
                                    ...highschoolStudentsData.value,
                                    ...data,
                                ];

                                if (status.value === Status.TERMINATED) {
                                    highschoolStudentsData.value.length = 0;
                                    return;
                                }
                            }
                        });
                }),
            );

            if (status.value !== (Status.TERMINATED as Status))
                status.value = Status.COMPLETED;
        }

        if (store.reportType === ReportType.SABERPRO) {
            await Promise.all(
                Array.from({ length: totalPages }).map((_, pageIndex) => {
                    return fetchData(
                        {
                            endpoint: "/college/students_paginated/",
                            options: {
                                method: "POST",
                            },
                            body: {
                                department: store.department,
                                municipality: store.municipality,
                                college: store.institution,
                                period: store.period,
                                pageSize: STUDENTS_CHUNK_SIZE,
                            },
                        },
                        { page: pageIndex + 1 },
                    )
                        .then((response) =>
                            CollegeResponseArray.parse(response),
                        )
                        .then((data) => {
                            if (data.length) {
                                collegeStudentsData.value = [
                                    ...collegeStudentsData.value,
                                    ...data,
                                ];

                                if (status.value === Status.TERMINATED) {
                                    collegeStudentsData.value.length = 0;
                                    return;
                                }
                            }
                        });
                }),
            );

            if (status.value !== (Status.TERMINATED as Status))
                status.value = Status.COMPLETED;
        }

        if (status.value === Status.COMPLETED)
            toast({
                title: "Finished gathering the students data",
                description: "Action just finished",
            });
    }

    async function fetchData(
        { endpoint, options, body }: RequestArgs,
        { page }: Options,
    ) {
        const { $api } = useNuxtApp();

        const [error, response] = await withCatch(
            $api<unknown[]>(endpoint, {
                ...options,
                body: {
                    ...body,
                    page,
                },
            }),
        );

        if (error) {
            toast({
                title: "Oops! An error ocurred",
                description: JSON.stringify(error),
            });

            return;
        }

        return response;
    }

    onMounted(() => {
        watch(
            () => highschoolStudentsData.value.length,
            () => console.log(highschoolStudentsData.value.length),
        );
    });

    return {
        highschoolStudentsData,
        collegeStudentsData,
        execute,
    };
}
