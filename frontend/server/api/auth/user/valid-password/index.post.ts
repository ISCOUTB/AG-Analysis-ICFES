import { type H3Event, H3Error } from "h3";
import { prisma } from "@/lib/prisma";
import { compare } from "bcrypt";

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);
        const { password } = await readBody(event);

        const user = await prisma.user.findUnique({
            where: {
                id: session.user.id,
            },
        });

        if (!user)
            throw createError({
                statusCode: 400,
                statusMessage: "User not exists",
            });

        if (!user.hashedPassword)
            throw createError({
                statusCode: 400,
                statusMessage: "Wrong login method",
            });

        const isValidPassword = compare(password, user.hashedPassword);

        if (!isValidPassword)
            throw createError({
                statusCode: 400,
                statusMessage: "Wrong password",
            });

        return { isValidPassword };
    } catch (error) {
        if (error instanceof H3Error) throw createError({ ...error });

        throw createError({
            statusCode: 500,
            statusMessage: "An unknown error ocurred",
        });
    }
});
