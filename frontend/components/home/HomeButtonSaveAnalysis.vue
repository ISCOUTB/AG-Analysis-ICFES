<script setup lang="ts">
    import { useToast } from "@/components/ui/toast";

    function saveAnalysis() {
        const { toast } = useToast();
        const analyisStore = useAnalysisOptions();
        const refs = storeToRefs(analyisStore);

        $fetch("/api/analysis/save", {
            body: {
                department: refs.department.value,
                municipality: refs.municipality.value,
                institution: refs.institution.value,
                period: refs.period.value,
                reportType: analyisStore.reportType,
            },
            method: "POST",
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        })
            .then(() => {
                toast({
                    title: "Saved succesfully",
                });
            })
            .finally(async () => await refreshNuxtData("stored-analysis"));
    }
</script>

<template>
    <Button variant="outline" @click="saveAnalysis"> Save Analysis </Button>
</template>
