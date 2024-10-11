<script setup lang="ts">
    import { ChevronsUpDown } from "lucide-vue-next";
    import { useToast } from "@/components/ui/toast";
    import { ReportType } from "@/types/types";
    import type { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
    import type { z } from "zod";

    interface Props {
        savedItem: Partial<z.infer<typeof SaveAnalysisSchema>> & {
            id: string;
            createdAt: Date;
        };
    }

    const { savedItem } = defineProps<Props>();

    const isOpen = ref(false);

    const { toast } = useToast();

    const items: SheetSavedAnalysisCollapsibleItem[] = [
        {
            label: "Department",
            icon: "mdi:briefcase",
            classIcon: "text-3xl text-green-500/80",
            renderIf: !!savedItem.department,
            value: savedItem.department,
        },
        {
            label: "Municipality",
            icon: "mdi:land-fields",
            classIcon: "text-4xl text-sky-500",
            renderIf: !!savedItem.municipality,
            value: savedItem.municipality,
        },
        {
            label: "Highschool",
            icon: "hugeicons:student-card",
            classIcon: "text-4xl text-rose-500",
            renderIf: () => {
                if (savedItem.reportType === ReportType.SABER11) return true;
                return false;
            },
            value: savedItem.institution,
        },
        {
            label: "College",
            icon: "ph:student",
            classIcon: "text-4xl text-yellow-500",
            renderIf: () => {
                if (savedItem.reportType === ReportType.SABERPRO) return true;
                return false;
            },
            value: savedItem.institution,
        },
        {
            label: "Period",
            icon: "material-symbols:nest-clock-farsight-analog-outline-rounded",
            classIcon: "text-3xl text-violet-500",
            renderIf: !!savedItem.period,
            value: savedItem.period,
        },
    ];

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
                <SheetSavedAnalysisCollapsibleAlertDialog
                    :handle-delete="handleDelete"
                />

                <CollapsibleTrigger as-child>
                    <Button variant="ghost" size="sm" class="w-9 p-0">
                        <ChevronsUpDown class="h-4 w-4" />
                        <span class="sr-only">Toggle</span>
                    </Button>
                </CollapsibleTrigger>
            </div>
        </div>

        <CollapsibleContent class="space-y-2 mr-8">
            <template v-for="item in items" :key="item.label">
                <template v-if="item.renderIf">
                    <div
                        class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
                    >
                        <div
                            class="w-full h-full flex items-center justify-center"
                        >
                            <Icon :name="item.icon" :class="item.classIcon" />
                        </div>
                        <div class="flex flex-col">
                            <span class="font-medium text-sm">{{
                                item.label
                            }}</span>
                            <span class="text-sm text-gray-600">{{
                                item.value
                            }}</span>
                        </div>
                    </div>
                </template>
            </template>
        </CollapsibleContent>
    </Collapsible>
</template>
