import { useAnalysisOptions } from "@/stores/analysisOptions";
import {
    CollegeResponseArray,
    HighschoolResponseArray,
} from "@/schemas/analysis/students.schema";
import type { FetchOptions } from "ofetch";
import { ReportType, Status } from "@/types/types";
import { useToast } from "@/components/ui/toast";
import type { z } from "zod";

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
    const status = useState<Status>(() => Status.IDLE);
    const error = useState();
    const { toast } = useToast();

    const highschoolStudentsData =
        useState<z.infer<typeof HighschoolResponseArray>>();

    const collegeStudentsData =
        useState<z.infer<typeof CollegeResponseArray>>();

    async function execute() {
        status.value = Status.LOADING;

        if (store.reportType === ReportType.SABER11) {
            await fetchData(
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
                        pageSize: 1000,
                    },
                },
                {
                    page: 1,
                },
            )
                .catch((_error) => console.log(_error))
                .finally(() => {
                    status.value = status.value = Status.COMPLETED;
                    
                    toast({
                        title: "Getting the data for the students",
                        description: "Action just finished",
                    });
                });
        }

        if (store.reportType === ReportType.SABERPRO) {
            await fetchData(
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
                        pageSize: 1000,
                    },
                },
                {
                    page: 1,
                },
            )
                .catch((_error) => console.log(_error))
                .finally(() => {
                    status.value = status.value = Status.COMPLETED;
                    toast({
                        title: "Getting the data for the students",
                        description: "Action just finished",
                    });
                });
        }
    }

    async function fetchData(
        { endpoint, options, body }: RequestArgs,
        { page }: Options,
    ) {
        const { $api } = useNuxtApp();

        $api<unknown[]>(endpoint, {
            ...options,
            body: {
                ...body,
                page,
            },
        })
            .then((response) => {
                if (store.reportType === ReportType.SABER11) {
                    const data = HighschoolResponseArray.parse(response);

                    if (data.length) {
                        highschoolStudentsData.value = [
                            ...highschoolStudentsData.value,
                            ...data,
                        ];

                        fetchData(
                            { endpoint, options, body },
                            { page: page + 1 },
                        );
                    }
                }

                if (store.reportType === ReportType.SABERPRO) {
                    const data = CollegeResponseArray.parse(response);

                    if (data.length) {
                        collegeStudentsData.value = [
                            ...collegeStudentsData.value,
                            ...data,
                        ];

                        fetchData(
                            { endpoint, options, body },
                            { page: page + 1 },
                        );
                    }
                }
            })
            .catch((_error) => {
                error.value = _error;
                status.value = Status.ERROR;
            });
    }

    return {
        status,
        highschoolStudentsData,
        collegeStudentsData,
        execute,
    };
}
