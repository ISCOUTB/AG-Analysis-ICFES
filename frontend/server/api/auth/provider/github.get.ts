import type { H3Event } from "h3";
import { prisma } from "@/lib/prisma";

const provider: string = "github";

export default oauthGitHubEventHandler({
    onSuccess: async (event: H3Event, { user }) => {
        const providerAccountId: string = user.id.toString();

        const _userAccount = await getUserAccount({
            provider,
            providerAccountId,
        });

        if (!_userAccount) {
            const createdUser = await createUser(
                { name: user.login },
                { provider, providerAccountId },
            );

            await createUserAccount(
                { userId: createdUser.id },
                { provider, providerAccountId },
            );

            await setSession(event, {
                email: createdUser.email,
                id: createdUser.id,
                image: user.avatar_url,
                name: createdUser.name || user.name,
            });

            return sendRedirect(event, "/");
        }

        const _user = await prisma.user.findUnique({
            where: { id: _userAccount.userId },
        });

        if (!_user)
            throw createError({
                statusCode: 400,
                statusMessage: "User not exists",
            });

        await setSession(event, {
            email: _user.email,
            id: _user.id,
            image: user.avatar_url,
            name: _user.name || user.name,
        });

        return sendRedirect(event, "/");
    },
});
