import { H3Error, type H3Event } from "h3";
import { prisma } from "@/lib/prisma";

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);

        const { email, name } = await readBody(event);

        const userWithEmail = await prisma.user.findUnique({
            where: { email },
        });

        if (userWithEmail)
            throw createError({
                statusCode: 400,
                statusMessage: "Email already in use",
            });

        const user = await prisma.user.update({
            data: {
                email,
                name,
            },
            where: {
                id: session.user.id,
            },
        });

        await replaceUserSession(event, {
            user: {
                email: user.email,
                name: user.name || user.email.split("@")[0],
                id: user.id,
            },
            loggedInAt: Date.now(),
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
