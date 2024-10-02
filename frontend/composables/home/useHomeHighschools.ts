import { useAnalysisOptions } from "@/stores/analysisOptions";

export default function () {
    const analysisOptions = useAnalysisOptions();

    const municipalityId = computed(() => analysisOptions.municipality);

    const { data } = useAsyncGql({
        operation: "highschools",
        variables: {
            municipalityId,
        },
        options: {
            immediate: false,
            watch: [municipalityId],
        },
    });

    const filteredHighschools = computed(() => {
        if (!data.value) return [];

        return data.value.highschools?.filter(
            (highschool) => highschool !== null,
        );
    });

    return {
        filteredHighschools,
    };
}
