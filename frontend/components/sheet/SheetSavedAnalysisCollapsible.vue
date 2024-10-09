<script setup lang="ts">
    import type { SavedAnalysis } from "@prisma/client";
    import { ChevronsUpDown } from "lucide-vue-next";
    import { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
    import { useToast } from "@/components/ui/toast";
    import { ReportType } from "@/types/types";

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

    const { data: highschoolData, refresh: refreshHighschool } = useAsyncGql({
        operation: "highschool",
        variables: {
            id: parsedContent.institution,
        },
        options: {
            immediate: false,
        },
    });

    const { data: collegeData, refresh: refreshCollege } = useAsyncGql({
        operation: "college",
        variables: {
            id: parsedContent.institution,
        },
        options: {
            immediate: false,
        },
    });

    const { data: periodData, refresh: refreshPeriod } = useAsyncGql({
        operation: "period",
        variables: {
            id: parsedContent.period,
        },
        options: {
            immediate: false,
        },
    });

    const items: SheetSavedAnalysisCollapsibleItem[] = [
        {
            label: "Department",
            icon: "mdi:briefcase",
            classIcon: "text-3xl text-green-500/80",
            renderIf: computed(
                () =>
                    !(
                        !parsedContent.department ||
                        !departmentData.value ||
                        !departmentData.value.department ||
                        !departmentData.value.department.name
                    ),
            ),
            getValue() {
                if (!this.renderIf) return;
                return departmentData.value.department?.name;
            },
        },
        {
            label: "Municipality",
            icon: "mdi:land-fields",
            classIcon: "text-4xl text-sky-500",
            renderIf: computed(
                () =>
                    !(
                        !parsedContent.municipality ||
                        !municipalityData.value ||
                        !municipalityData.value.municipality ||
                        !municipalityData.value.municipality.name
                    ),
            ),
            getValue() {
                if (!this.renderIf) return;
                return municipalityData.value.municipality?.name;
            },
        },
        {
            label: "Highschool",
            icon: "hugeicons:student-card",
            classIcon: "text-4xl text-rose-500",
            renderIf: computed(() => {
                if (parsedContent.reportType !== ReportType.SABER11)
                    return false;

                return !(
                    (!parsedContent.institution ||
                        !highschoolData.value ||
                        !highschoolData.value.highschool ||
                        !highschoolData.value.highschool.name) &&
                    parsedContent.reportType === ReportType.SABER11
                );
            }),
            getValue() {
                if (!this.renderIf) return;
                return highschoolData.value.highschool?.name;
            },
        },
        {
            label: "College",
            icon: "ph:student",
            classIcon: "text-4xl text-yellow-500",
            renderIf: computed(() => {
                if (parsedContent.reportType !== ReportType.SABERPRO)
                    return false;

                return !(
                    (!parsedContent.institution ||
                        !collegeData.value ||
                        !collegeData.value.college ||
                        !collegeData.value.college.name) &&
                    parsedContent.reportType === ReportType.SABERPRO
                );
            }),
            getValue() {
                if (!this.renderIf) return;
                return collegeData.value.college?.name;
            },
        },
        {
            label: "Period",
            icon: "material-symbols:nest-clock-farsight-analog-outline-rounded",
            classIcon: "text-3xl text-violet-500",
            renderIf: computed(
                () =>
                    !(
                        !parsedContent.period ||
                        !periodData.value ||
                        !periodData.value.period ||
                        !periodData.value.period.label
                    ),
            ),
            getValue() {
                if (!this.renderIf) return;
                return periodData.value.period?.label;
            },
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

    onMounted(() => {
        watch(isOpen, (newValue) => {
            if (!newValue) return;

            if (!departmentData.value) refreshDeparment();

            if (!municipalityData.value) refreshMunicipality();

            switch (parsedContent.reportType) {
                case ReportType.SABER11:
                    if (!highschoolData.value) refreshHighschool();
                    break;

                case ReportType.SABERPRO:
                    if (!collegeData.value) refreshCollege();
                    break;
            }

            if (!periodData.value) refreshPeriod();
        });
    });
</script>
.value
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
                <template v-if="item.renderIf.value">
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
                                item.getValue()
                            }}</span>
                        </div>
                    </div>
                </template>
            </template>
        </CollapsibleContent>
    </Collapsible>
</template>
