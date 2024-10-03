<script setup lang="ts">
    import type { SavedAnalysis } from "@prisma/client";
    import { ChevronsUpDown } from "lucide-vue-next";
    import { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
    import { useToast } from "@/components/ui/toast";

    interface Props {
        savedItem: SavedAnalysis;
    }

    const { savedItem } = defineProps<Props>();

    const isOpen = ref(false);
    const parsedContent = SaveAnalysisSchema.parse(
        JSON.parse(savedItem.content),
    );
    const { toast } = useToast();

    const { data: departmentData, refresh: refreshDeparment } = useAsyncGql({
        operation: "department",
        variables: {
            id: parsedContent.department,
        },
        options: {
            immediate: false,
        },
    });

    const { data: municipalityData, refresh: refreshMunicipality } =
        useAsyncGql({
            operation: "municipality",
            variables: {
                id: parsedContent.municipality,
            },
            options: {
                immediate: false,
            },
        });

        

    watch(isOpen, (newValue) => {
        if (!newValue) return;

        if (!departmentData.value || !municipalityData.value)
            Promise.all([refreshDeparment(), refreshMunicipality()]);
    });

    function handleDelete() {
        $fetch("/api/analysis/saved/deleted", {
            query: {
                analysisId: savedItem.id,
            },
            method: "POST",
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        })
            .then(() => {
                toast({
                    title: "Deleted succesfully",
                });
            })
            .finally(async () => await refreshNuxtData("stored-analysis"));
    }
</script>

<template>
    <Collapsible v-model:open="isOpen" class="w-[350px] space-y-2">
        <div
            class="flex items-center justify-between mr-4 px-4 py-1 rounded-md"
        >
            <h4 class="text-sm font-semibold">
                {{
                    new Date(savedItem.createdAt).toLocaleString("en-Es", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                    })
                }}
            </h4>

            <div>
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
                            <AlertDialogTitle
                                >Are you absolutely sure?</AlertDialogTitle
                            >
                            <AlertDialogDescription>
                                This will remove the stored info from our
                                servers and cannot be undone
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

                <CollapsibleTrigger as-child>
                    <Button variant="ghost" size="sm" class="w-9 p-0">
                        <ChevronsUpDown class="h-4 w-4" />
                        <span class="sr-only">Toggle</span>
                    </Button>
                </CollapsibleTrigger>
            </div>
        </div>

        <CollapsibleContent class="space-y-2 mr-8">
            <div
                v-if="parsedContent.department && departmentData.department"
                class="rounded-md border px-4 py-3 text-sm flex items-center space-x-3"
            >
                <Icon name="mdi:briefcase" class="text-3xl text-green-500" />
                <div class="flex flex-col">
                    <span class="font-medium text-sm">Department</span>
                    <span class="text-sm text-gray-600">{{
                        departmentData.department.name
                    }}</span>
                </div>
            </div>
            <div
                v-if="
                    parsedContent.municipality && municipalityData.municipality
                "
                class="rounded-md border px-4 py-3 text-sm flex items-center space-x-3"
            >
                <Icon name="mdi:land-fields" class="text-3xl text-sky-500" />
                <div class="flex flex-col">
                    <span class="font-medium text-sm">Municipality</span>
                    <span class="text-sm text-gray-600">{{
                        municipalityData.municipality.name
                    }}</span>
                </div>
            </div>
        </CollapsibleContent>
    </Collapsible>
</template>
