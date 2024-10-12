<script setup lang="ts">
    import type { SavedAnalysis } from "@prisma/client";
    import { ReportType } from "~/types/types";
    import { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";

    const parsedData = useState<SheetSavedAnalysisParsedData[]>("parsed-data");

    async function getInstitutionInfo(item: SheetSavedAnalysisData) {
        if (item.reportType === ReportType.SABER11) {
            const { highschool } = await GqlHighschool({
                id: item.institution,
            });

            return highschool?.name;
        }

        if (item.reportType === ReportType.SABERPRO) {
            const { college } = await GqlCollege({ id: item.institution });

            return college?.name;
        }
    }

    async function handleClick() {
        $fetch<SavedAnalysis[]>("/api/analysis/saved", {
            cache: "force-cache",
        })
            .then((results) => {
                return results.map((item) => ({
                    ...item,
                    content: SaveAnalysisSchema.parse(JSON.parse(item.content)),
                }));
            })
            .then((data) =>
                data.map((item) => ({
                    content: item.content,
                    id: item.id,
                    createdAt: item.createdAt,
                })),
            )
            .then(async (data) => {
                parsedData.value = data.map((item) => ({
                    id: item.id,
                    createdAt: item.createdAt,
                    content: {},
                }));

                await Promise.all(
                    data.map(async (item, index) => {
                        if (item.content.department) {
                            const { department } = await GqlDepartment({
                                id: item.content.department,
                            });

                            parsedData.value[index].content.department =
                                department?.name;
                        }

                        if (item.content.municipality) {
                            const { municipality } = await GqlMunicipality({
                                id: item.content.institution,
                            });

                            parsedData.value[index].content.municipality =
                                municipality?.name;
                        }

                        if (item.content.institution) {
                            parsedData.value[index].content.institution =
                                await getInstitutionInfo(item.content);
                        }

                        if (item.content.period) {
                            const { period } = await GqlPeriod({
                                id: item.content.period,
                            });

                            parsedData.value[index].content.period =
                                period?.label;
                        }

                        parsedData.value[index].content.reportType =
                            item.content.reportType;
                    }),
                );
            });
    }
</script>

<template>
    <Sheet>
        <SheetTrigger as-child>
            <Button variant="outline" @click="handleClick">
                Show stored analysis
            </Button>
        </SheetTrigger>
        <SheetContent class="overflow-y-auto overflow-x-hidden">
            <SheetHeader>
                <SheetTitle>Stored Analysis</SheetTitle>
            </SheetHeader>
            <div class="flex flex-col gap-4">
                <template v-if="parsedData">
                    <SheetSavedAnalysisCollapsible
                        v-for="item in parsedData"
                        :key="item.id"
                        :saved-item="item"
                    />
                </template>
            </div>
        </SheetContent>
    </Sheet>
</template>
