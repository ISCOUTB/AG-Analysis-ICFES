<script setup>
    import { ReportType, StudentsCountStatus } from "@/types/types";
    import { useToast } from "@/components/ui/toast";

    onMounted(() => {
        const store = useAnalysisOptions();
        const { department, municipality, institution } = storeToRefs(store);
        const { toast } = useToast();

        watch(
            [department, municipality, institution],
            () => {
                store.setStudentsCountStatus(StudentsCountStatus.LOADING);

                if (store.reportType === ReportType.SABER11) {
                    GqlHighschoolStudentsCount({
                        departmentId: department.value,
                        municipalityId: municipality.value,
                        highschoolId: institution.value,
                    })
                        .then((value) => value.highschoolStudentsCount)
                        .then((value) => store.setStudentsCount(value || 100))
                        .finally(() =>
                            store.setStudentsCountStatus(
                                StudentsCountStatus.COMPLETED,
                            ),
                        );

                    return;
                }

                if (store.reportType === ReportType.SABERPRO) {
                    GqlCollegeStudentsCount({
                        departmentId: department.value,
                        municipalityId: municipality.value,
                        collegeId: institution.value,
                    })
                        .then((value) => value.collegeStudentsCount)
                        .then((value) => store.setStudentsCount(value || 100))
                        .finally(() =>
                            store.setStudentsCountStatus(
                                StudentsCountStatus.COMPLETED,
                            ),
                        );

                    return;
                }
            },
            {
                deep: true,
            },
        );

        watch(
            () => store.studentsCountStatus,
            () => {
                if (store.studentsCountStatus === StudentsCountStatus.COMPLETED)
                    toast({
                        title: "You can go ahead now ;)",
                    });
            },
        );
    });
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
        <Toaster />
    </NuxtLayout>
</template>
