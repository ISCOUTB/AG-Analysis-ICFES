import { prisma } from "@/lib/prisma";
import type { Account } from "@prisma/client";

export default async function (
    { userId  }: UserInfo,
    { provider, providerAccountId }: ProviderInfo,
): Promise<Account> {
    return await prisma.account.create({
        data: {
            userId,
            provider,
            providerAccountId,
        },
    });
}