<script setup lang="ts">
    const { parsedData, reload } = useSavedAnalysis() 
</script>

<template>
    <Sheet>
        <SheetTrigger as-child>
            <Button variant="outline" @click="reload">
                Show stored analysis
            </Button>
        </SheetTrigger>
        <SheetContent class="overflow-y-auto overflow-x-hidden">
            <SheetHeader>
                <SheetTitle>Stored Analysis</SheetTitle>
            </SheetHeader>
            <div class="flex flex-col gap-4 mt-4">
                <template v-if="parsedData">
                    <SheetSavedAnalysisCollapsible
                        v-for="item in parsedData"
                        :key="item.id"
                        :saved-item="item"
                    />
                </template>
            </div>
        </SheetContent>
    </Sheet>
</template>
