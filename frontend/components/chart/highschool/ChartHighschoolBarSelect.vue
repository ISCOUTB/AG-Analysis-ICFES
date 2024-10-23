<script setup lang="ts">
    const { highschoolGroupBy } = await useStudents();
</script>

<template>
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
</template>
