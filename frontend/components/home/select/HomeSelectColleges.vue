<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { data } = await useHomeColleges();
    const disabled = computed(
        () => !analysisStore.municipality || !data.value?.length,
    );

    async function handleSelect(payload: string) {
        analysisStore.setInstitution(payload);
    }
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
                    v-for="item in data"
                    :key="item.id"
                    :value="item.id.toString()"
                >
                    {{ item.name }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
