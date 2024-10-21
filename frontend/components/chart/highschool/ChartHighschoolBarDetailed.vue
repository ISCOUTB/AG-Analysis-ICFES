<script setup lang="ts">
    const { highschoolGroupBy } = await useStudents();
</script>

<template>
    <template
        v-for="highschoolId in Object.keys(highschoolGroupBy)"
        :key="highschoolId"
    >
        <ChartHighschoolBarDetailedCollapsible
            :highschool-id="highschoolId"
            :items="highschoolGroupBy[highschoolId]"
        />
    </template>
</template>
