<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { filteredMunicipalities } = useHomeMunicipalities();
    const disabled = computed(
        () =>
            !analysisStore.department || !filteredMunicipalities.value?.length,
    );

    function handleSelect(payload: string) {
        analysisStore.setMunicipality(payload);
        analysisStore.clear("institution");
    }
</script>

<template>
    <div>
        <span class="font-semibold">Municipality</span>
        <Select
            :model-value="analysisStore.municipality"
            :disabled="disabled"
            @update:model-value="handleSelect"
        >
            <SelectTrigger class="mt-2">
                <SelectValue placeholder="Select a Municipality" />
            </SelectTrigger>
            <SelectContent>
                <div>
                    <SelectItem
                        v-for="data in filteredMunicipalities"
                        :key="data.id"
                        :value="data.id"
                    >
                        {{ data.name }}
                    </SelectItem>
                </div>
            </SelectContent>
        </Select>
    </div>
</template>
