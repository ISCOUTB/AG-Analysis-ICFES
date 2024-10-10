<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    const { filteredHighschools } = useHomeHighschools();
    const disabled = computed(
        () => !analysisStore.municipality || !filteredHighschools.value?.length,
    );

    async function handleSelect(payload: string) {
        analysisStore.setInstitution(payload);

        const { highschoolStudentsCount } = await GqlHighschoolStudentsCount({
            highschoolId: analysisStore.institution,
        });

        analysisStore.setStudentsCount(highschoolStudentsCount || 100);
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
                    v-for="item in filteredHighschools"
                    :key="item.id"
                    :value="item.id"
                >
                    {{ item.name }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
