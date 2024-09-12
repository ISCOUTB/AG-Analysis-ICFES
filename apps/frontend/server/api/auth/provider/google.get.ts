import type { H3Event } from "h3";
import { prisma } from "@/lib/prisma";

const provider: string = "google";

export default oauthGoogleEventHandler({
    onSuccess: async (event: H3Event, { user }) => {
        const providerAccountId: string = user.sub.toString();

        const _userAccount = await getUserAccount({
            provider,
            providerAccountId,
        });

        if (!_userAccount) {
            const createdUser = await createUser(
                { name: user.name, email: user.email },
                { provider, providerAccountId },
            );

            await createUserAccount(
                { userId: createdUser.id },
                { provider, providerAccountId },
            );

            await setSession(event, {
                email: createdUser.email,
                name: createdUser.name || user.name,
                id: createdUser.id,
                image: user.picture,
            });

            return sendRedirect(event, "/");
        }

        const _user = await prisma.user.findUnique({
            where: {
                id: _userAccount.userId,
            },
        });

        if (!_user)
            throw createError({
                statusCode: 400,
                statusMessage: "User not exists",
            });

        await setSession(event, {
            email: _user.email,
            name: _user.name || user.name,
            id: _user.id,
            image: user.picture,
        });

        return sendRedirect(event, "/");
    },
});
