<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { data } = await useHomeMunicipalities();
    const disabled = computed(
        () => !analysisStore.department || !data.value?.length,
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
                        v-for="item in data"
                        :key="item.id"
                        :value="item.id.toString()"
                    >
                        {{ item.name }}
                    </SelectItem>
                </div>
            </SelectContent>
        </Select>
    </div>
</template>
