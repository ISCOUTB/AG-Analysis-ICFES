import { H3Error } from "h3";
import { prisma } from "@/lib/prisma";
import { hash, genSalt } from "bcrypt";

const hashPassword = async (password: string) => {
    const salt = await genSalt(15);
    return await hash(password, salt);
};

export default defineEventHandler(async (event) => {
    try {
        const { email, password, name } = await readBody(event);

        const userWithEmail = await prisma.user.findUnique({
            where: { email },
        });

        if (userWithEmail)
            throw createError({
                statusCode: 400,
                statusMessage: "Email already in use",
            });

        const hashedPassword = await hashPassword(password);

        const user = await prisma.user.create({
            data: {
                email,
                hashedPassword,
                name,
            },
        });

        return { user };
    } catch (error) {
        if (error instanceof H3Error) throw createError({ ...error });

        throw createError({
            statusCode: 500,
            message: "An unknown error ocurred",
        });
    }
});
