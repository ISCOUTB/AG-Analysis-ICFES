<script setup lang="ts">
    useHead({
        title: "Home Page",
    });
</script>

<template>
    <section :key="$route.fullPath">
        <HomeAnalysisOptions />
        <HomeAditionalOptions />
        <div class="w-full bg-background py-12">
            <div class="container px-4 md:px-6">
                <Button> Submit </Button>
            </div>
        </div>
    </section>
</template>
