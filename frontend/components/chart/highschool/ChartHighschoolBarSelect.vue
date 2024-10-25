<script setup lang="ts">
    import { capitalize } from "lodash";

    interface Response {
        name: string;
    }

    const { highschoolGroupBy } = await useStudents();
    const { department: departmentId, municipality: municipalityId } =
        useAnalysisOptions();
    const { $api } = useNuxtApp();

    const { data: department } = useFetch<Response>(
        `/department/${departmentId}`,
        { $fetch: $api },
    );

    const { data: municipality } = useFetch<Response>(
        `/municipality/${municipalityId}`,
        { $fetch: $api },
    );
</script>

<template>
    <div class="space-y-6">
        <Separator label="Select Institution and Period" />
        <ChartDescription class="text-center">
            Institutions registered in {{ capitalize(department?.name) }},
            {{ capitalize(municipality?.name) }}. Each institutions have data of
            multiple periods, select one of them in order to continue.
        </ChartDescription>
        <ScrollArea
            class="h-64 w-full rounded-lg border-2 border-gray-300/30 shadow dark:border-gray-400/20 p-4"
        >
            <template
                v-for="highschoolId in Object.keys(highschoolGroupBy)"
                :key="highschoolId"
            >
                <ChartHighschoolBarSelectCollapsible
                    :highschool-id="highschoolId"
                    :items="highschoolGroupBy[highschoolId]"
                    class="mb-4 last:mb-0"
                />
            </template>
        </ScrollArea>
    </div>
</template>
