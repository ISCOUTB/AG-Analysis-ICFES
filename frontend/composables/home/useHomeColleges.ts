import { useAnalysisOptions } from "@/stores/analysisOptions";

export default function () {
    const analysisOptions = useAnalysisOptions();

    const municipalityId = computed(() => analysisOptions.municipality);

    const { data } = useAsyncGql({
        operation: "colleges",
        variables: {
            municipalityId,
        },
        options: {
            immediate: false,
            watch: [municipalityId],
        },
    });

    const filteredColleges = computed(() => {
        if (!data.value) return [];

        return data.value.colleges?.filter((college) => college !== null);
    });

    return {
        filteredColleges,
    };
}
