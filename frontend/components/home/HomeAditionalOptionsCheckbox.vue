<script setup lang="ts">
    interface Props {
        label: string;
        description?: string;
        action: () => unknown;
    }

    const { label, description, action } = defineProps<Props>();
    const id = useId();
</script>

<template>
    <div class="items-top flex gap-x-2">
        <Checkbox :id="id" @update:checked="action" />
        <div class="grid gap-1.5 leading-none">
            <label
                :for="id"
                class="text-sm font-semibold leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
                {{ label }}
            </label>
            <p v-if="description" class="text-sm text-muted-foreground">
                {{ description }}
            </p>
        </div>
    </div>
</template>
