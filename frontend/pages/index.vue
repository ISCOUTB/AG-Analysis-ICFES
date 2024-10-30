<script setup lang="ts">
    import { ReportType, Status } from "@/types/types";
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Home Page",
    });

    const { status } = useStatus();
    const { toast } = useToast();
    const store = useAnalysisOptions();
    const { progress } = await useHomeProgress();
    const { currentTask } = useHomeCurrentTask();
    const { startDriver } = useDriver();

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
    <section :key="$route.fullPath" v-auto-animate>
        <HomeAnalysisOptions />
        <div class="w-full py-12 bg-gray-300/20 dark:bg-gray-900/80">
            <div
                v-auto-animate
                class="container px-4 md:px-6 flex flex-wrap gap-2"
            >
                <Button
                    id="select-options__submit"
                    :disabled="status === Status.LOADING"
                    @click="handleSubmit"
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
                <Button variant="ghost" @click="startDriver">
                    Start Tutorial
                </Button>
            </div>
        </div>
        <template v-if="status === Status.IDLE">
            <div class="w-full bg-gray-300/20 dark:bg-gray-900/80 mt-4">
                <div
                    class="container px-4 md:px-6 py-6 text-sm font-medium opacity-60"
                >
                    <span>Once submited you can view your results here</span>
                </div>
            </div>
        </template>
        <template v-if="status === Status.LOADING">
            <div
                class="w-full flex items-center justify-center mt-12 flex-col gap-2"
            >
                <div class="w-4/5">
                    <Progress :model-value="progress" :max="100" />
                </div>
                <div
                    class="animate-pulse text-gray-800 dark:text-gray-500 text-sm flex flex-col items-center"
                >
                    <span>{{ currentTask }}</span>
                    <span> Loading: {{ roundToDecimals(progress, 2) }}% </span>
                </div>
            </div>
        </template>
        <template v-if="status === Status.COMPLETED">
            <div class="w-full mt-4">
                <template v-if="store.reportType === ReportType.SABER11">
                    <div
                        class="container px-4 md:px-6 py-6 flex flex-col gap-8"
                    >
                        <ChartHighschoolBar />
                        <ChartHighschoolTable />
                        <ChartHighschoolBarSelect />
                        <ChartHighschoolHistogram />
                    </div>
                </template>

                <template v-if="store.reportType === ReportType.SABERPRO">
                    <div
                        class="container px-4 md:px-6 py-6 flex flex-col gap-8"
                    >
                        <ChartCollegeBar />
                        <ChartCollegeTable />
                        <ChartCollegeBarSelect />
                        <ChartCollegeHistogram />
                    </div>
                </template>
            </div>
        </template>
        <template v-if="status === Status.TERMINATED">
            <div
                class="w-full mt-4 bg-gray-950 dark:bg-slate-50 text-slate-50 dark:text-gray-950"
            >
                <div
                    class="container px-4 md:px-6 py-6 flex text-sm font-medium"
                >
                    Analysis Terminated
                </div>
            </div>
        </template>
    </section>
</template>
