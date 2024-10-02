import { H3Error, type H3Event } from "h3";
import { prisma } from "@/lib/prisma";
import { genSalt, hash } from "bcrypt";

export default defineEventHandler(async (event: H3Event) => {
    try {
        const session = await requireUserSession(event);
        const { password } = await readBody(event);

        if (!password)
            throw createError({
                statusCode: 400,
                statusMessage: "No password were provided",
            });

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

        const salt = await genSalt(15);
        const hashedPassword = await hash(password, salt);

        const updatedUser = await prisma.user.update({
            where: {
                id: user.id,
            },
            data: {
                hashedPassword,
            },
        });

        return { updatedUser };
    } catch (error) {
        if (error instanceof H3Error) throw createError({ ...error });

        throw createError({
            statusCode: 500,
            statusMessage: "An unknown error ocurred",
        });
    }
});
