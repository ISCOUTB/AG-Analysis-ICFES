import { z } from "zod";
import { ReportType } from "@/types/types";
import { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
import type { SavedAnalysis } from "@prisma/client";

export default function () {
    const parsedData = useState<SheetSavedAnalysisParsedData[]>("parsed-data");

    async function getInstitutionInfo(item: SheetSavedAnalysisData) {
        const Response = z.object({
            name: z.string(),
        });

        const { $api } = useNuxtApp();

        if (item.reportType === ReportType.SABER11) {
            const response = await $api<unknown>(
                `/highschool/${item.institution}`,
            );
            const data = Response.parse(response);
            return data.name;
        }

        if (item.reportType === ReportType.SABERPRO) {
            const response = await $api<unknown>(
                `/college/${item.institution}`,
            );
            const data = Response.parse(response);
            return data.name;
        }
    }

    async function reload() {
        $fetch<SavedAnalysis[]>("/api/analysis/saved")
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

                const { $api } = useNuxtApp();

                await Promise.all(
                    data.map(async (item, index) => {
                        if (item.content.department) {
                            const Response = z.object({
                                name: z.string(),
                            });

                            const response = await $api<unknown>(
                                `/department/${item.content.department}`,
                            );

                            const data = Response.parse(response);

                            parsedData.value[index].content.department =
                                data.name;
                        }

                        if (item.content.municipality) {
                            const Response = z.object({
                                name: z.string(),
                            });

                            const response = await $api<unknown>(
                                `/municipality/${item.content.municipality}`,
                            );

                            const data = Response.parse(response);

                            parsedData.value[index].content.municipality =
                                data.name;
                        }

                        if (item.content.institution) {
                            parsedData.value[index].content.institution =
                                await getInstitutionInfo(item.content);
                        }

                        if (item.content.period) {
                            const Response = z.object({
                                label: z.string(),
                            });

                            const response = await $api(
                                `/period/${item.content.period}`,
                            );

                            const data = Response.parse(response);

                            parsedData.value[index].content.period = data.label;
                        }

                        parsedData.value[index].content.reportType =
                            item.content.reportType;
                    }),
                );
            });
    }

    return {
        parsedData,
        reload,
    };
}
