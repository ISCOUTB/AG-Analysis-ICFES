<script setup lang="ts">
    const { collegeGroupBy } = await useStudents();
</script>

<template>
    <ScrollArea
        class="h-64 w-full rounded-lg border-2 border-gray-300/30 shadow dark:border-gray-400/20 p-4"
    >
        <template
            v-for="collegeId in Object.keys(collegeGroupBy)"
            :key="collegeId"
        >
            <ChartCollegeBarSelectCollapsible
                :college-id="collegeId"
                :items="collegeGroupBy[collegeId]"
                class="mb-4 last:mb-0"
            />
        </template>
    </ScrollArea>
</template>
