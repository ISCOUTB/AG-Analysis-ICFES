import { H3Error, H3Event } from "h3";
import { z } from "zod";
import { ReportType } from "@/types/types";
import { prisma } from "@/lib/prisma";
import isEqual from "lodash/isEqual";

const requestBody = z.object({
    department: z.string(),
    municipality: z.string(),
    institution: z.string(),
    period: z.string(),
    reportType: z.nativeEnum(ReportType),
});

const normalizeContent = (content: string) =>
    requestBody.parse(JSON.parse(content));

async function shouldSave(
    parsedBody: z.infer<typeof requestBody>,
    userId: string,
): Promise<boolean> {
    const allStored = await prisma.savedAnalysis.findMany({
        where: {
            userId,
        },
    });

    if (!allStored || allStored.length === 0) return true;

    return allStored.reduce((_, currentValue) => {
        const parsedContent = normalizeContent(currentValue.content);
        return !isEqual(parsedBody, parsedContent);
    }, true);
}

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);
        const body = await readBody(event);
        const parsedBody = requestBody.parse(body);

        if (!session.user.id)
            throw createError({
                statusCode: 400,
                statusMessage: "Invalid user",
            });

        const save = await shouldSave(parsedBody, session.user.id);

        if (!save)
            throw createError({
                statusCode: 400,
                statusMessage: "Analysis already stored",
            });

        await prisma.savedAnalysis.create({
            data: {
                content: JSON.stringify({ ...parsedBody }),
                userId: session.user.id,
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
