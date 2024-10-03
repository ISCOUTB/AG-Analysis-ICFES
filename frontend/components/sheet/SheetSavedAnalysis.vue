<script setup lang="ts">
    import type { SavedAnalysis } from "@prisma/client";

    const { data } = useFetch<SavedAnalysis[]>("/api/analysis/saved", {
        key: "stored-analysis",
    });
</script>

<template>
    <Sheet>
        <SheetTrigger>
            <Button variant="secondary"> Show stored analysis </Button>
        </SheetTrigger>
        <SheetContent class="overflow-y-auto overflow-x-hidden">
            <SheetHeader>
                <SheetTitle>Stored Analysis</SheetTitle>
            </SheetHeader>
            <div class="flex flex-col gap-4">
                <SheetSavedAnalysisCollapsible
                    v-for="item in data"
                    :key="item.id"
                    :saved-item="item"
                />
            </div>
        </SheetContent>
    </Sheet>
</template>
