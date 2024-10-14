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
    const municipalityId = computed(() => analysisOptions.municipality);

    return useAsyncData<z.infer<typeof ResponseArray>>(
        "colleges",
        () => {
            if (!municipalityId.value) return Promise.resolve([]);

            return $api(`/municipality/${municipalityId.value}/colleges`)
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
        { immediate: false, watch: [municipalityId] },
    );
}
