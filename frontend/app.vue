<script setup>
    import { ReportType, StudentsCountStatus } from "@/types/types";
    import { z } from "zod";

    const Response = z.object({
        count: z.number(),
    });

    const store = useAnalysisOptions();
    const { department, municipality, institution, period } =
        storeToRefs(store);
    const { reload } = useSavedAnalysis();

    function reloadStudentsCount() {
        const { $api } = useNuxtApp();

        store.setStudentsCountStatus(StudentsCountStatus.LOADING);

        if (store.reportType === ReportType.SABER11) {
            $api("/highschool/students_count/", {
                method: "POST",
                body: {
                    department: department.value,
                    municipality: municipality.value,
                    highschool: institution.value,
                    period: period.value,
                },
            })
                .then((response) => Response.parse(response))
                .then(({ count }) => store.setStudentsCount(count || 100))
                .finally(() =>
                    store.setStudentsCountStatus(StudentsCountStatus.COMPLETED),
                );

            return;
        }

        if (store.reportType === ReportType.SABERPRO) {
            $api("/college/students_count/", {
                method: "POST",
                body: {
                    department: department.value,
                    municipality: municipality.value,
                    highschool: institution.value,
                    period: period.value,
                },
            })
                .then((response) => Response.parse(response))
                .then(({ count }) => store.setStudentsCount(count || 100))
                .finally(() =>
                    store.setStudentsCountStatus(StudentsCountStatus.COMPLETED),
                );

            return;
        }
    }

    onMounted(() => {
        watch([department, municipality, institution, period], () =>
            reloadStudentsCount(),
        );

        reload();
        reloadStudentsCount();
    });
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
        <Toaster />
    </NuxtLayout>
</template>
