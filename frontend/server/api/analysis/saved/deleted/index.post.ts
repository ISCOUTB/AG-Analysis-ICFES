import { H3Error, type H3Event } from "h3";
import { prisma } from "@/lib/prisma";

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);
        const { analysisId } = getQuery(event);

        if (!analysisId)
            throw createError({
                statusCode: 400,
                statusMessage: ":analysisId must be provided",
            });

        const savedAnalysis = await prisma.savedAnalysis.findUnique({
            where: {
                id: analysisId.toString(),
            },
        });

        if (!savedAnalysis)
            throw createError({
                statusCode: 400,
                statusMessage: "SavedAnalysis does not exists",
            });

        if (savedAnalysis.userId !== session.user.id)
            throw createError({
                statusCode: 400,
                statusMessage: "You're not the owner of this",
            });

        await prisma.savedAnalysis.delete({
            where: {
                id: savedAnalysis.id,
            },
        });

        return {};
    } catch (error) {
        if (error instanceof H3Error) throw createError({ ...error });

        throw createError({
            statusCode: 500,
            statusMessage: "An unknown error ocurred",
        });
    }
});
