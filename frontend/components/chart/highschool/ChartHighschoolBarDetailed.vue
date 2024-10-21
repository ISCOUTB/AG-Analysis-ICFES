<script setup lang="ts">
    const { highschoolGroupBy } = await useStudents();
</script>

<template>
    <ScrollArea class="h-64 w-full rounded-md border-2 border-emerald-500 p-4">
        <template
            v-for="highschoolId in Object.keys(highschoolGroupBy)"
            :key="highschoolId"
        >
            <ChartHighschoolBarDetailedCollapsible
                :highschool-id="highschoolId"
                :items="highschoolGroupBy[highschoolId]"
                class="mb-4 last:mb-0"
            />
        </template>
    </ScrollArea>
</template>
