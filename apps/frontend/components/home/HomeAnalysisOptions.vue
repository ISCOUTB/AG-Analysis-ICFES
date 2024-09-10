<script setup lang="ts">
    import { useAnalysisOptions, ReportType } from "@/stores/analysisOptions";

    const analysisStore = useAnalysisOptions();

    function handleReportTypeChange(payload: string | number) {
        const value = payload.toString();

        if (value !== ReportType.SABER11 && value !== ReportType.SABERPRO)
            return;

        analysisStore.setReportType(value);
    }
</script>

<template>
    <section class="w-full bg-background py-12">
        <div
            class="container px-4 md:px-6 flex flex-col md:grid md:grid-cols-2 gap-4"
        >
            <div class="flex flex-col gap-8">
                <div class="flex flex-col gap-4">
                    <span class="text-3xl font-bold">Advanced Analysis</span>
                    <span class="text-gray-600 dark:text-slate-50/70"
                        >Personalize your analysis options to obtain more
                        meaninful insights.</span
                    >
                </div>
                <div>
                    <span class="font-semibold">Report Type</span>
                    <Select @update:model-value="handleReportTypeChange">
                        <SelectTrigger class="mt-2">
                            <SelectValue placeholder="Select the Report Type" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem
                                v-for="type in ReportType"
                                :key="type"
                                :value="type"
                            >
                                {{ type }}
                            </SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>
            <div class="flex flex-col gap-4">
                <div>
                    <span class="font-semibold">Department</span>
                    <Select
                        :model-value="analysisStore.department"
                        @update:model-value="
                            (payload: string) =>
                                analysisStore.setDepartment(payload)
                        "
                    >
                        <SelectTrigger class="mt-2">
                            <SelectValue placeholder="Select a Department" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="value"> Buenos dias </SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <div>
                    <span class="font-semibold">Municipality</span>
                    <Select
                        :model-value="analysisStore.municipality"
                        @update:model-value="
                            (payload: string) => analysisStore.setMunicipality(payload)
                        "
                    >
                        <SelectTrigger class="mt-2">
                            <SelectValue placeholder="Select a Municipality" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="value"> Buenos dias </SelectItem>
                        </SelectContent>
                    </Select>
                </div>
                <div>
                    <span class="font-semibold">Institution</span>
                    <Select
                        :model-value="analysisStore.institution"
                        @update:model-value="
                            (payload: string) => analysisStore.setInstitution(payload)
                        "
                    >
                        <SelectTrigger class="mt-2">
                            <SelectValue placeholder="Select a Institution" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="value"> Buenos dias </SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>
        </div>
    </section>
</template>
