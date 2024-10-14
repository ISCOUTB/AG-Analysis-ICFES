import { useAnalysisOptions } from "@/stores/analysisOptions";
import { z } from "zod";
import { ReportType } from "~/types/types";

const Response = z.object({
    id: z.number(),
    label: z.string(),
});

const ResponseArray = z.array(Response);

function getQuery(reportType: ReportType): string {
    switch (reportType) {
        case ReportType.SABER11:
            return "/highschool/periods/";
        case ReportType.SABERPRO:
            return "/college/periods/";
    }
}

export default async function () {
    const analysisOptions = useAnalysisOptions();
    const { $api } = useNuxtApp();
    const reportType = computed(() => analysisOptions.reportType);

    return useAsyncData(
        "municipalities",
        () =>
            $api(getQuery(analysisOptions.reportType))
                .then((response) => ResponseArray.parse(response))
                .catch((error) => {
                    if (error instanceof z.ZodError)
                        throw createError({
                            statusCode: 500,
                            statusMessage: error.message,
                        });
                }),
        { immediate: false, watch: [reportType] },
    );
}
