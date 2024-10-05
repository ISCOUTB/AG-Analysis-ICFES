<script setup lang="ts">
    import type { SavedAnalysis } from "@prisma/client";
    import { ChevronsUpDown } from "lucide-vue-next";
    import { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
    import { useToast } from "@/components/ui/toast";
    import { ReportType } from "@/types/types";
    import type { HtmlHTMLAttributes } from "vue";

    interface Props {
        savedItem: SavedAnalysis;
    }

    interface Item {
        label: string;
        value?: string;
        icon: string;
        iconClass: HtmlHTMLAttributes["class"];
        renderIf: boolean;
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

    const items = computed<Item[]>(() => [
        {
            label: "Department",
            value: departmentData.value.department?.name,
            icon: "mdi:briefcase",
            iconClass: "text-3xl text-green-500/80",
            renderIf: !!(
                parsedContent.department && departmentData.value.department
            ),
        },
        {
            label: "Municipality",
            value: municipalityData.value.municipality?.name,
            icon: "mdi:land-fields",
            iconClass: "text-4xl text-sky-500",
            renderIf: !!(
                parsedContent.municipality &&
                municipalityData.value.municipality
            ),
        },
        {
            label: "Highschool",
            value: highschoolData.value.highschool?.name,
            icon: "hugeicons:student-card",
            iconClass: "text-4xl text-rose-500",
            renderIf: !!(
                parsedContent.institution &&
                highschoolData.value.highschool &&
                parsedContent.reportType === ReportType.SABER11
            ),
        },
        {
            label: "College",
            value: collegeData.value.college?.name,
            icon: "ph:student",
            iconClass: "text-4xl text-yellow-500",
            renderIf: !!(
                parsedContent.institution &&
                collegeData.value.college &&
                parsedContent.reportType === ReportType.SABERPRO
            ),
        },
        {
            label: "Period",
            value: periodData.value.period?.label,
            icon: "material-symbols:nest-clock-farsight-analog-outline-rounded",
            iconClass: "text-3xl text-violet-500",
            renderIf: !!(parsedContent.period && periodData.value.period),
        },
    ]);

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
            <!-- <div
                v-if="parsedContent.department && departmentData.department"
                class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
            >
                <div class="w-full h-full flex items-center justify-center">
                    <Icon
                        name="mdi:briefcase"
                        class="text-3xl text-green-500/80"
                    />
                </div>
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
                class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
            >
                <div class="w-full h-full flex items-center justify-center">
                    <Icon
                        name="mdi:land-fields"
                        class="text-4xl text-sky-500"
                    />
                </div>
                <div class="flex flex-col">
                    <span class="font-medium text-sm">Municipality</span>
                    <span class="text-sm text-gray-600">{{
                        municipalityData.municipality.name
                    }}</span>
                </div>
            </div>
            <template v-if="parsedContent.reportType === ReportType.SABER11">
                <div
                    v-if="
                        parsedContent.institution && highschoolData.highschool
                    "
                    class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
                >
                    <div class="w-full h-full flex items-center justify-center">
                        <Icon
                            name="hugeicons:student-card"
                            class="text-4xl text-rose-500"
                        />
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium text-sm">Highschool</span>
                        <span class="text-sm text-gray-600">{{
                            highschoolData.highschool.name
                        }}</span>
                    </div>
                </div>
            </template>
            <template v-if="parsedContent.reportType === ReportType.SABERPRO">
                <div
                    v-if="parsedContent.institution && collegeData.college"
                    class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
                >
                    <div class="w-full h-full flex items-center justify-center">
                        <Icon
                            name="ph:student"
                            class="text-4xl text-yellow-500"
                        />
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium text-sm">College</span>
                        <span class="text-sm text-gray-600">{{
                            collegeData.college.name
                        }}</span>
                    </div>
                </div>
            </template>
            <div
                v-if="parsedContent.period && periodData.period"
                class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
            >
                <div class="w-full h-full flex items-center justify-center">
                    <Icon
                        name="material-symbols:nest-clock-farsight-analog-outline-rounded"
                        class="text-3xl text-violet-500"
                    />
                </div>
                <div class="flex flex-col">
                    <span class="font-medium text-sm">Period</span>
                    <span class="text-sm text-gray-600">{{
                        periodData.period.label
                    }}</span>
                </div>
            </div> -->

            <template v-for="item in items" :key="item.label">
                <div
                    v-if="item.renderIf"
                    class="rounded-md border pl-1 py-3 text-sm grid grid-cols-[1fr_4fr] items-start justify-items-start"
                >
                    <div class="w-full h-full flex items-center justify-center">
                        <Icon :name="item.icon" :class="item.iconClass" />
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
        </CollapsibleContent>
    </Collapsible>
</template>
