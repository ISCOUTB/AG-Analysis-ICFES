import { H3Error } from "h3";
import { prisma } from "@/lib/prisma";
import { compare } from "bcrypt";

export default eventHandler(async (event) => {
    try {
        const { email, password } = await readBody(event);

        if (!email || !password)
            throw createError({
                statusCode: 400,
                statusMessage: "Invalid Request",
            });

        const user = await prisma.user.findUnique({ where: { email } });

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

        const isValidPassword = await compare(
            password.toString(),
            user.hashedPassword,
        );

        if (!isValidPassword)
            throw createError({
                statusCode: 400,
                statusMessage: "Wrong password",
            });

        await setUserSession(event, {
            user: {
                id: user.id,
                email: user.email,
                name: user.name || user.email.split("@")[0],
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
