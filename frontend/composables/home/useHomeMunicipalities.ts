import { useAnalysisOptions } from "@/stores/analysisOptions";

export default function () {
    const analysisOptions = useAnalysisOptions();

    const departmentId = computed(() => analysisOptions.department);

    const { data } = useAsyncGql({
        operation: "municipalities",
        variables: {
            departmentId,
        },
        options: {
            immediate: false,
            watch: [departmentId],
        },
    });

    const filteredMunicipalities = computed(() => {
        if (!data.value) return [];

        return data.value.municipalities?.filter(
            (department) => department !== null,
        );
    });

    return {
        filteredMunicipalities,
    };
}
