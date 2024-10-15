<script setup>
    const { reload } = useSavedAnalysis();

    onMounted(() => reload());
</script>

<template>
    <NuxtLayout>
        <NuxtPage />
        <Toaster />
    </NuxtLayout>
</template>
