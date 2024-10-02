<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { filteredColleges } = useHomeColleges();
    const disabled = computed(
        () => !analysisStore.municipality || !filteredColleges.value?.length,
    );

    const handleSelect = (payload: string) =>
        analysisStore.setInstitution(payload);
</script>

<template>
    <div>
        <span class="font-semibold">Institution</span>
        <Select
            :model-value="analysisStore.institution"
            :disabled="disabled"
            @update:model-value="handleSelect"
        >
            <SelectTrigger class="mt-2">
                <SelectValue placeholder="Select a Institution" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem
                    v-for="item in filteredColleges"
                    :key="item.id"
                    :value="item.id"
                >
                    {{ item.name }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
