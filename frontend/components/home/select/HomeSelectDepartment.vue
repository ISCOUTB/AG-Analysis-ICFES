<script setup lang="ts">
    import { useAnalysisOptions } from "@/stores/analysisOptions";
    import { z } from "zod";

    const Response = z.object({
        id: z.number(),
        name: z.string(),
    });

    const ResponseArray = z.array(Response);

    const analysisStore = useAnalysisOptions();

    const { $api } = useNuxtApp();

    const { data } = await useAsyncData<unknown>(() => $api("/department/"));

    const parsedData = computed(() => ResponseArray.parse(data.value));

    function handleSelect(payload: string) {
        analysisStore.setDepartment(payload);
        analysisStore.clear("municipality");
        analysisStore.clear("institution");
    }
</script>

<template>
    <div key="HomeSelectDepartment">
        <span class="font-semibold">Department</span>
        <Select
            :model-value="analysisStore.department"
            @update:model-value="handleSelect"
        >
            <SelectTrigger class="mt-2">
                <SelectValue placeholder="Select a department" />
            </SelectTrigger>
            <SelectContent>
                <SelectItem
                    v-for="department in parsedData"
                    :key="department.id"
                    :value="department.id.toString()"
                >
                    {{ department.name }}
                </SelectItem>
            </SelectContent>
        </Select>
    </div>
</template>
