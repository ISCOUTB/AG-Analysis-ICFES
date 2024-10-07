<script setup lang="ts">
    useHead({
        title: "Home Page",
    });
</script>

<template>
    <section :key="$route.fullPath">
        <HomeAnalysisOptions />
        <div class="w-full py-12 bg-gray-300/20 dark:bg-gray-900/80">
            <div class="container px-4 md:px-6 flex gap-2">
                <Button> Submit </Button>
                <HomeButtonSaveAnalysis />
                <SheetSavedAnalysis />
            </div>
        </div>
    </section>
</template>
