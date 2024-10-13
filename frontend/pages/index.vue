<script setup lang="ts">
    useHead({
        title: "Home Page",
    });

    const { status, execute } =
        await useStudents();

    async function handleSubmit() {
        execute();
    }
</script>

<template>
    <section :key="$route.fullPath">
        <HomeAnalysisOptions />
        <div class="w-full py-12 bg-gray-300/20 dark:bg-gray-900/80">
            <div class="container px-4 md:px-6 flex gap-2">
                <Button @click="handleSubmit"> Submit </Button>
                <HomeButtonSaveAnalysis />
                <SheetSavedAnalysis />
            </div>
        </div>
        <div class="w-full bg-gray-300/20 dark:bg-gray-900/80 mt-4">
            <div
                class="container px-4 md:px-6 py-6 flex gap-2 text-sm font-medium opacity-60"
            >
                <span>Once submited you can view your results here</span>
            </div>
        </div>
        {{ status }}
    </section>
</template>
