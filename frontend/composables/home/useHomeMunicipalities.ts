import { useAnalysisOptions } from "@/stores/analysisOptions";
import { z } from "zod";

const Response = z.object({
    id: z.number(),
    name: z.string(),
});

const ResponseArray = z.array(Response);

export default async function () {
    const analysisOptions = useAnalysisOptions();
    const { $api } = useNuxtApp();
    const departmentId = computed(() => analysisOptions.department);

    return useAsyncData<z.infer<typeof ResponseArray>>(
        "municipalities",
        () => {
            if (!departmentId.value) return Promise.resolve([]);

            return $api(`/department/${departmentId.value}/municipalities`)
                .then((response) => ResponseArray.parse(response))
                .catch((error) => {
                    if (error instanceof z.ZodError)
                        throw createError({
                            statusCode: 500,
                            statusMessage: error.message,
                        });

                    throw createError({
                        statusCode: 500,
                        statusMessage: JSON.stringify(error),
                    });
                });
        },
        { immediate: false, watch: [departmentId] },
    );
}
