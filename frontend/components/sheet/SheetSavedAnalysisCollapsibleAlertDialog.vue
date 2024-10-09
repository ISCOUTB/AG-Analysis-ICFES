<script setup lang="ts">
    interface Props {
        handleDelete: () => void;
    }

    defineProps<Props>();
</script>

<template>
    <AlertDialog>
        <AlertDialogTrigger>
            <Button class="bg-inherit px-3 hover:bg-rose-500 group">
                <Icon
                    name="mdi:trash-can-outline"
                    class="text-lg text-rose-500 group-hover:text-slate-50"
                />
            </Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
            <AlertDialogHeader>
                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                <AlertDialogDescription>
                    This will remove the stored info from our servers and cannot
                    be undone
                </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction @click="handleDelete"
                    >Continue</AlertDialogAction
                >
            </AlertDialogFooter>
        </AlertDialogContent>
    </AlertDialog>
</template>
