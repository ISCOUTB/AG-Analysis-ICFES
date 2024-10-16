import { useAnalysisOptions } from "@/stores/analysisOptions";
import {
    CollegeResponseArray,
    HighschoolResponseArray,
} from "@/schemas/analysis/students.schema";
import type { FetchOptions } from "ofetch";
import { ReportType, Status } from "@/types/types";
import { useToast } from "@/components/ui/toast";
import type { z } from "zod";
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

    const highschoolStudentsData = useState<
        z.infer<typeof HighschoolResponseArray>
    >(() => []);

    const collegeStudentsData = useState<z.infer<typeof CollegeResponseArray>>(
        () => [],
    );

    async function execute() {
        status.value = Status.LOADING;

        if (store.reportType === ReportType.SABER11) {
            async function loop(page: number) {
                const response = await fetchData(
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
                    { page: page },
                );

                const data = HighschoolResponseArray.parse(response);

                if (data.length) {
                    highschoolStudentsData.value = [
                        ...highschoolStudentsData.value,
                        ...data,
                    ];

                    if (status.value === Status.TERMINATED) {
                        highschoolStudentsData.value.length = 0;
                        return;
                    }

                    await loop(page + 1);
                }
            }

            await loop(1);

            if (status.value !== (Status.TERMINATED as Status))
                status.value = Status.COMPLETED;
        }

        if (store.reportType === ReportType.SABERPRO) {
            async function loop(page: number) {
                const response = await fetchData(
                    {
                        endpoint: "/college/students_paginated",
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
                    { page: page },
                );

                const data = CollegeResponseArray.parse(response);

                if (data.length) {
                    collegeStudentsData.value = [
                        ...collegeStudentsData.value,
                        ...data,
                    ];

                    if (status.value === Status.TERMINATED) {
                        collegeStudentsData.value.length = 0;
                        return;
                    }

                    await loop(page + 1);
                }
            }

            await loop(1);

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

        try {
            const response = await $api<unknown[]>(endpoint, {
                ...options,
                body: {
                    ...body,
                    page,
                },
            });

            return response;
        } catch (error) {
            throw createError({
                statusCode: 500,
                statusMessage: JSON.stringify(error),
            });
        }
    }

    return {
        highschoolStudentsData,
        collegeStudentsData,
        execute,
    };
}
