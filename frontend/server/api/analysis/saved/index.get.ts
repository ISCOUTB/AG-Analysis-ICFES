import { H3Error, type H3Event } from "h3";
import { prisma } from "@/lib/prisma";

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);

        return await prisma.savedAnalysis.findMany({
            where: {
                userId: session.user.id,
            },
        });
    } catch (error) {
        if (error instanceof H3Error) throw createError({ ...error });

        throw createError({
            statusCode: 500,
            statusMessage: "An unknown error ocurred",
        });
    }
});
