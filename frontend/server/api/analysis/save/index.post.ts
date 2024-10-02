import { H3Error, H3Event } from "h3";
import { z } from "zod";
import { ReportType } from "@/types/types";
import { prisma } from "@/lib/prisma";

const requestBody = z.object({
    department: z.string(),
    municipality: z.string(),
    institution: z.string(),
    period: z.string(),
    reportType: z.nativeEnum(ReportType),
});

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);
        const body = await readBody(event);
        const parsedBody = requestBody.parse(body);

        if (!session.user.id)
            throw createError({
                statusCode: 400,
                statusMessage: "|error| invalid user",
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
