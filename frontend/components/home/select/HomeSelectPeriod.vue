<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { data } = await useHomePeriods();
</script>

<template>
    <div id="select-options__period" key="HomeSelectPeriod">
        <span class="font-semibold">Period</span>
        <Select
            :model-value="analysisStore.period"
            @update:model-value="(payload) => analysisStore.setPeriod(payload)"
        >
            <SelectTrigger class="mt-2">
                <SelectValue placeholder="Select a period" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem
                    v-for="item in data"
                    :key="item.id"
                    :value="item.id.toString()"
                >
                    {{ item.label }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
