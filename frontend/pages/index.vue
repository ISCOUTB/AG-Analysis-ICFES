<script setup lang="ts">
    import { ReportType, Status } from "@/types/types";
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Home Page",
    });

    const { execute } = await useStudents();
    const { status } = useStatus();
    const { toast } = useToast();
    const store = useAnalysisOptions();

    function handleTerminate() {
        status.value = Status.TERMINATED;

        toast({
            title: "Process Terminated",
            description: "U・ﻌ・U",
            variant: "destructive",
        });
    }
</script>

<template>
    <section :key="$route.fullPath">
        <HomeAnalysisOptions />
        <div class="w-full py-12 bg-gray-300/20 dark:bg-gray-900/80">
            <div v-auto-animate class="container px-4 md:px-6 flex gap-2">
                <Button
                    :disabled="status === Status.LOADING"
                    @click="async () => await execute()"
                >
                    Submit
                </Button>
                <HomeButtonSaveAnalysis />
                <SheetSavedAnalysis />
                <Button
                    v-if="status === Status.LOADING"
                    variant="destructive"
                    @click.once="handleTerminate"
                    >Cancel</Button
                >
            </div>
        </div>
        <div
            v-if="status !== Status.COMPLETED"
            v-auto-animate
            class="w-full bg-gray-300/20 dark:bg-gray-900/80 mt-4"
        >
            <div
                class="container px-4 md:px-6 py-6 flex gap-2 text-sm font-medium opacity-60"
            >
                <span>Once submited you can view your results here</span>
            </div>
        </div>
        <template v-if="status === Status.COMPLETED">
            <div class="w-full mt-4">
                <template v-if="store.reportType === ReportType.SABER11">
                    <div
                        class="container px-4 md:px-6 py-6 flex flex-col gap-8"
                    >
                        <LazyChartHighschoolBar />
                        <LazyChartHighschoolTable />
                    </div>
                </template>

                <template v-if="store.reportType === ReportType.SABERPRO">
                    <div
                        class="container px-4 md:px-6 py-6 flex flex-col gap-8"
                    >
                        <LazyChartCollegeBar />
                        <LazyChartCollegeTable />
                    </div>
                </template>
            </div>
        </template>
    </section>
</template>
