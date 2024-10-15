<script setup lang="ts">
    import { Status } from "@/types/types";
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Home Page",
    });

    const { execute } = await useStudents();
    const { status } = useStatus();
    const { toast } = useToast();

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
        <div class="w-full bg-gray-300/20 dark:bg-gray-900/80 mt-4">
            <div
                class="container px-4 md:px-6 py-6 flex gap-2 text-sm font-medium opacity-60"
            >
                <span>Once submited you can view your results here</span>
            </div>
        </div>
    </section>
</template>
